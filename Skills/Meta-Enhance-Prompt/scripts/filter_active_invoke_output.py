#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from filter_prompt_shape_helper import DEFAULT_TEMPLATE, load_template, missing_required_sections, parse_contract_sections, render_contract, validate_final_shape
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


def _emit_error(code: int, message: str, as_json: bool, *, mode_decision: str) -> int:
    payload = {"mode_decision": mode_decision, "filter_exit_code": code, "filter_exit_message": message, "publish_blocked": True}
    mode = mode_decision.removesuffix("_mode") or "runtime_error"
    run_id = new_run_id(mode)
    rendered_output = json.dumps(payload, ensure_ascii=False) + "\n"
    artifact_path = write_output_artifact(mode=mode, rendered_output=rendered_output, as_json=True, output_path=None)
    log_paths = attach_runtime_logs(run_id=run_id, mode=mode, status="error", output_path=artifact_path, payload=payload)
    payload["run_id"] = run_id
    payload["output_path"] = str(artifact_path)
    payload["runtime_logs"] = log_paths
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    else:
        sys.stderr.write(message + "\n")
    return code


def _persist_and_emit(*, payload: RuntimePayloadRecord, rendered_output: str, as_json: bool, output_path: str | None, mode: str) -> int:
    run_id = new_run_id(mode)
    artifact_path = write_output_artifact(mode=mode, rendered_output=rendered_output, as_json=as_json, output_path=output_path)
    log_paths = attach_runtime_logs(run_id=run_id, mode=mode, status="ok", output_path=artifact_path, payload=payload)
    payload["run_id"] = run_id
    payload["output_path"] = str(artifact_path)
    payload["runtime_logs"] = log_paths
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(rendered_output)
    return EXIT_SUCCESS


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter prompt output into a fixed structured execution contract or emit a skill read directive.")
    parser.add_argument("--mode", default="active_invoke", help="Supported: active_invoke, skill_directive.")
    parser.add_argument("--input-file", help="Path to raw prompt output.")
    parser.add_argument("--input-text", help="Raw prompt text.")
    parser.add_argument("--template-file", default=str(DEFAULT_TEMPLATE), help="Template file path.")
    parser.add_argument("--output-path", help="Optional explicit output artifact path.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON payload.")
    args = parser.parse_args()

    try:
        raw_input = _read_input(args)
    except (OSError, ValueError) as exc:
        return _emit_error(EXIT_INVALID_OUTPUT, f"invalid_output: {exc}", args.json, mode_decision=f"{args.mode}_mode")

    if args.mode == "skill_directive":
        code, message, payload = build_skill_directive(raw_input)
        if code != EXIT_SUCCESS:
            return _emit_error(code, message, args.json, mode_decision="skill_directive_mode")
        final_output = str(payload.get("final_skill_read_directive", "") or "")
        response_payload = {
            "mode_decision": "skill_directive_mode",
            "final_skill_read_directive": final_output,
            "filter_exit_code": code,
            "filter_exit_message": message,
            "publish_blocked": False,
            "resolved_skills": payload.get("resolved_skills", []),
            "intent_summary": payload.get("intent_summary", ""),
        }
        if args.json:
            rendered_output = json.dumps(response_payload, ensure_ascii=False) + "\n"
        else:
            rendered_output = final_output
        return _persist_and_emit(
            payload=response_payload,
            rendered_output=rendered_output,
            as_json=args.json,
            output_path=args.output_path,
            mode="skill_directive",
        )

    if args.mode != "active_invoke":
        return _emit_error(EXIT_INVALID_OUTPUT, "invalid_output: unsupported mode", args.json, mode_decision="unknown_mode")
    if not raw_input.strip():
        return _emit_error(EXIT_EMPTY_AFTER_FILTER, "empty_after_filter", args.json, mode_decision="active_invoke_mode")

    try:
        template = load_template(pathlib.Path(args.template_file).expanduser().resolve())
    except FileNotFoundError:
        return _emit_error(10, "template_missing", args.json, mode_decision="active_invoke_mode")
    except ValueError:
        return _emit_error(10, "template_missing_required_tokens", args.json, mode_decision="active_invoke_mode")

    sections = parse_contract_sections(raw_input)
    missing_sections = missing_required_sections(sections)
    if missing_sections:
        return _emit_error(
            EXIT_INVALID_OUTPUT,
            f"invalid_output: missing_required_sections={','.join(missing_sections)}",
            args.json,
            mode_decision="active_invoke_mode",
        )
    final_prompt = render_contract(template, sections)
    if not validate_final_shape(final_prompt):
        return _emit_error(EXIT_INVALID_OUTPUT, "invalid_output: forbidden token leak or missing header", args.json, mode_decision="active_invoke_mode")
    response_payload = {
        "mode_decision": "active_invoke_mode",
        "final_prompt_copy_paste": final_prompt,
        "filter_exit_code": EXIT_SUCCESS,
        "filter_exit_message": "success",
        "publish_blocked": False,
    }
    if args.json:
        rendered_output = json.dumps(response_payload, ensure_ascii=False) + "\n"
    else:
        rendered_output = final_prompt
    return _persist_and_emit(
        payload=response_payload,
        rendered_output=rendered_output,
        as_json=args.json,
        output_path=args.output_path,
        mode="active_invoke",
    )


if __name__ == "__main__":
    raise SystemExit(main())
