#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from filter_prompt_shape_helper import (
    DEFAULT_TEMPLATE,
    load_template,
    missing_required_sections,
    parse_intent_source,
    render_intent_output,
    resolve_intent_body,
    validate_final_shape,
)
from filter_runtime_governance import RuntimePayloadRecord, attach_runtime_logs, new_run_id, write_output_artifact
from filter_skill_directive_support import EXIT_EMPTY_AFTER_FILTER, EXIT_INVALID_OUTPUT, EXIT_SUCCESS, build_skill_directive


def _read_input(args: argparse.Namespace) -> str:
    if args.input_file and args.input_text:
        raise ValueError("provide only one of --input-file or --input-text")
    if args.input_file:
        return pathlib.Path(args.input_file).expanduser().resolve().read_text(encoding="utf-8")
    if args.input_text is not None:
        return args.input_text
    return sys.stdin.read()


def _canonical_mode(raw_mode: str) -> str:
    normalized = str(raw_mode or "").strip().lower()
    if not normalized:
        return "intent_clarify"
    if normalized == "active_invoke":
        return "intent_clarify"
    return normalized


def _emit_error(code: int, message: str, as_json: bool, *, mode_decision: str, artifact_mode: str) -> int:
    payload = {"mode_decision": mode_decision, "filter_exit_code": code, "filter_exit_message": message, "publish_blocked": True}
    run_id = new_run_id(artifact_mode)
    log_paths = attach_runtime_logs(run_id=run_id, mode=artifact_mode, status="error", output_path=pathlib.Path("publish_blocked"), payload=payload)
    payload["run_id"] = run_id
    payload["runtime_logs"] = log_paths
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    else:
        sys.stderr.write(message + "\n")
    return code


def _persist_and_emit(
    *,
    payload: RuntimePayloadRecord,
    publication_output: str,
    stdout_output: str,
    as_json: bool,
    output_path: str | None,
    mode: str,
) -> int:
    run_id = new_run_id(mode)
    artifact_path = write_output_artifact(mode=mode, rendered_output=publication_output, output_path=output_path)
    log_paths = attach_runtime_logs(run_id=run_id, mode=mode, status="ok", output_path=artifact_path, payload=payload)
    payload["run_id"] = run_id
    payload["output_path"] = str(artifact_path)
    payload["runtime_logs"] = log_paths
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(stdout_output)
    return EXIT_SUCCESS


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter intent clarification output or emit a skill read directive.")
    parser.add_argument("--mode", default="intent_clarify", help="Supported: intent_clarify, active_invoke, skill_directive.")
    parser.add_argument("--input-file", help="Path to raw prompt output.")
    parser.add_argument("--input-text", help="Raw prompt text.")
    parser.add_argument("--template-file", default=str(DEFAULT_TEMPLATE), help="Template file path.")
    parser.add_argument("--output-path", help="Optional explicit output artifact path.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON payload.")
    args = parser.parse_args()

    requested_mode = str(args.mode or "")
    mode = _canonical_mode(requested_mode)

    try:
        raw_input = _read_input(args)
    except (OSError, ValueError) as exc:
        failure_mode = "skill_directive" if mode == "skill_directive" else "intent_clarify"
        return _emit_error(EXIT_INVALID_OUTPUT, f"invalid_output: {exc}", args.json, mode_decision=f"{failure_mode}_mode", artifact_mode=failure_mode)

    if mode == "skill_directive":
        code, message, payload = build_skill_directive(raw_input)
        if code != EXIT_SUCCESS:
            return _emit_error(code, message, args.json, mode_decision="skill_directive_mode", artifact_mode="skill_directive")
        final_output = str(payload.get("final_skill_read_directive", "") or "")
        response_payload = {
            "mode_decision": "skill_directive_mode",
            "final_skill_read_directive": final_output,
            "filter_exit_code": code,
            "filter_exit_message": message,
            "publish_blocked": False,
            "resolved_skills": payload.get("resolved_skills", []),
            "intent_summary": payload.get("intent_summary", ""),
            "session_context_detected": bool(payload.get("session_context_detected", False)),
            "chat_publish_policy": "When publishing a final intent output in chat, do not prepend another paraphrase outside the INTENT block.",
        }
        return _persist_and_emit(
            payload=response_payload,
            publication_output=final_output,
            stdout_output=final_output,
            as_json=args.json,
            output_path=args.output_path,
            mode="skill_directive",
        )

    if mode != "intent_clarify":
        return _emit_error(EXIT_INVALID_OUTPUT, "invalid_output: unsupported mode", args.json, mode_decision="unknown_mode", artifact_mode="unknown_mode")
    if not raw_input.strip():
        return _emit_error(EXIT_EMPTY_AFTER_FILTER, "empty_after_filter", args.json, mode_decision="intent_clarify_mode", artifact_mode="intent_clarify")

    try:
        template = load_template(pathlib.Path(args.template_file).expanduser().resolve())
    except FileNotFoundError:
        return _emit_error(10, "template_missing", args.json, mode_decision="intent_clarify_mode", artifact_mode="intent_clarify")
    except ValueError:
        return _emit_error(10, "template_missing_required_tokens", args.json, mode_decision="intent_clarify_mode", artifact_mode="intent_clarify")

    parsed, preprocess_metadata = parse_intent_source(raw_input)
    intent_body = resolve_intent_body(parsed)
    missing_sections = missing_required_sections(intent_body)
    if missing_sections:
        return _emit_error(
            EXIT_INVALID_OUTPUT,
            f"invalid_output: missing_required_sections={','.join(missing_sections)}",
            args.json,
            mode_decision="intent_clarify_mode",
            artifact_mode="intent_clarify",
        )
    final_intent_output = render_intent_output(template, intent_body)
    if not validate_final_shape(final_intent_output):
        return _emit_error(
            EXIT_INVALID_OUTPUT,
            "invalid_output: forbidden token leak or missing INTENT header",
            args.json,
            mode_decision="intent_clarify_mode",
            artifact_mode="intent_clarify",
        )
    response_payload = {
        "mode_decision": "intent_clarify_mode",
        "final_intent_output": final_intent_output,
        "final_prompt_copy_paste": final_intent_output,
        "extracted_intent": intent_body,
        "context_session_refs": preprocess_metadata.get("context_session_refs", []),
        "context_request_detected": bool(preprocess_metadata.get("context_request_detected", False)),
        "target_prompt_detected": bool(preprocess_metadata.get("target_prompt_detected", False)),
        "target_prompt_source": preprocess_metadata.get("target_prompt_source", "raw_input"),
        "filter_exit_code": EXIT_SUCCESS,
        "filter_exit_message": "success",
        "publish_blocked": False,
        "chat_publish_policy": "If the final intent output is published in chat or referenced via output_path, do not prepend another restatement outside the INTENT block.",
    }
    return _persist_and_emit(
        payload=response_payload,
        publication_output=final_intent_output,
        stdout_output=final_intent_output,
        as_json=args.json,
        output_path=args.output_path,
        mode="intent_clarify",
    )


if __name__ == "__main__":
    raise SystemExit(main())
