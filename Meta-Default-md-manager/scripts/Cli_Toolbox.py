#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_parser_support import build_parser
from managed_collect import collect_from_scan
from managed_guidance import load_runtime_contract, load_stage_directive, render_audit_docs
from managed_lock import acquire_cli_lock
from managed_paths import resolve_skill_root, resolve_source_root
from managed_push import push_out
from managed_registry import load_registry
from managed_scan import resolve_scan_source_root, write_scan_report
from managed_target_runtime import load_target_contract


def print_payload(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    for key, value in payload.items():
        print(f"{key}: {value}")
    return 0


def cmd_registry(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    payload = load_registry(skill_root)
    payload["skill_root"] = str(skill_root)
    return print_payload(payload, args.json)


def cmd_contract(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    payload = load_runtime_contract(skill_root)
    return print_payload(payload, args.json)


def cmd_directive(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    payload = load_stage_directive(skill_root, args.stage)
    return print_payload(payload, args.json)


def cmd_target_contract(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    payload = load_target_contract(skill_root, args.source_path)
    return print_payload(payload, args.json)


def cmd_render_audit_docs(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    payload = render_audit_docs(skill_root)
    return print_payload(payload, args.json)


def cmd_scan(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    source_root = resolve_scan_source_root(args.source_root)
    with acquire_cli_lock(skill_root, "scan"):
        payload = write_scan_report(skill_root=skill_root, source_root=source_root)
    return print_payload(payload, args.json)


def cmd_collect(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    source_root = resolve_source_root(args.source_root) if args.source_root else None
    with acquire_cli_lock(skill_root, "collect"):
        payload = collect_from_scan(skill_root=skill_root, source_root=str(source_root) if source_root else None)
    return print_payload(payload, args.json)


def cmd_push(args) -> int:
    if not args.all and not args.target_source_path:
        raise SystemExit("pass --all or at least one --target-source-path")
    skill_root = resolve_skill_root(args.skill_root)
    with acquire_cli_lock(skill_root, "push"):
        payload = push_out(
            skill_root=skill_root,
            target_source_paths=args.target_source_path,
            push_all=args.all,
        )
    return print_payload(payload, args.json)


def main() -> int:
    parser = build_parser(
        cmd_registry,
        cmd_scan,
        cmd_collect,
        cmd_push,
        cmd_contract,
        cmd_directive,
        cmd_target_contract,
        cmd_render_audit_docs,
    )
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
