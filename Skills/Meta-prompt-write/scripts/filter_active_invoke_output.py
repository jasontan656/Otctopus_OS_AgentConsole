#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from filter_prompt_shape_helper import DEFAULT_TEMPLATE, load_template, parse_contract_sections, render_contract, validate_final_shape
from filter_skill_directive_support import EXIT_EMPTY_AFTER_FILTER, EXIT_INVALID_OUTPUT, EXIT_SKILL_SOURCE_MISSING, EXIT_SUCCESS, build_skill_directive


def _read_input(args: argparse.Namespace) -> str:
    if args.input_file and args.input_text:
        raise ValueError("provide only one of --input-file or --input-text")
    if args.input_file:
        return pathlib.Path(args.input_file).expanduser().resolve().read_text(encoding="utf-8")
    if args.input_text is not None:
        return args.input_text
    return sys.stdin.read()


def _emit_error(code: int, message: str, as_json: bool) -> int:
    payload = {"mode_decision": "active_invoke_mode", "filter_exit_code": code, "filter_exit_message": message, "publish_blocked": True}
    if as_json:
        sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    else:
        sys.stderr.write(message + "\n")
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter prompt output into a fixed structured execution contract or emit a skill read directive.")
    parser.add_argument("--mode", default="active_invoke", help="Supported: active_invoke, skill_directive.")
    parser.add_argument("--input-file", help="Path to raw prompt output.")
    parser.add_argument("--input-text", help="Raw prompt text.")
    parser.add_argument("--template-file", default=str(DEFAULT_TEMPLATE), help="Template file path.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON payload.")
    args = parser.parse_args()

    try:
        raw_input = _read_input(args)
    except Exception as exc:
        return _emit_error(EXIT_INVALID_OUTPUT, f"invalid_output: {exc}", args.json)

    if args.mode == "skill_directive":
        code, message, payload = build_skill_directive(raw_input)
        if code != EXIT_SUCCESS:
            return _emit_error(code, message, args.json)
        final_output = str(payload.get("final_skill_read_directive", "") or "")
        if args.json:
            sys.stdout.write(json.dumps({"mode_decision": "skill_directive_mode", "final_skill_read_directive": final_output, "filter_exit_code": code, "filter_exit_message": message, "publish_blocked": False, "resolved_skills": payload.get("resolved_skills", []), "intent_summary": payload.get("intent_summary", "")}, ensure_ascii=False) + "\n")
        else:
            sys.stdout.write(final_output)
        return EXIT_SUCCESS

    if args.mode != "active_invoke":
        return _emit_error(EXIT_INVALID_OUTPUT, "invalid_output: unsupported mode", args.json)
    if not raw_input.strip():
        return _emit_error(EXIT_EMPTY_AFTER_FILTER, "empty_after_filter", args.json)

    try:
        template = load_template(pathlib.Path(args.template_file).expanduser().resolve())
    except FileNotFoundError:
        return _emit_error(10, "template_missing", args.json)
    except ValueError:
        return _emit_error(10, "template_missing_required_tokens", args.json)

    final_prompt = render_contract(template, parse_contract_sections(raw_input))
    if not validate_final_shape(final_prompt):
        return _emit_error(EXIT_INVALID_OUTPUT, "invalid_output: forbidden token leak or missing header", args.json)
    if args.json:
        sys.stdout.write(json.dumps({"mode_decision": "active_invoke_mode", "final_prompt_copy_paste": final_prompt, "filter_exit_code": EXIT_SUCCESS, "filter_exit_message": "success", "publish_blocked": False}, ensure_ascii=False) + "\n")
    else:
        sys.stdout.write(final_prompt)
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
