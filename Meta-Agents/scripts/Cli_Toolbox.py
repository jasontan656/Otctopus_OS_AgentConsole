#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from cli_parser_support import build_parser
from managed_collect import collect_agents
from managed_paths import resolve_skill_root, resolve_source_root
from managed_registry import load_registry
from managed_sync import sync_out


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


def cmd_scan_collect(args) -> int:
    skill_root = resolve_skill_root(args.skill_root)
    source_root = resolve_source_root(args.source_root)
    payload = collect_agents(skill_root=skill_root, source_root=source_root)
    return print_payload(payload, args.json)


def cmd_sync_out(args) -> int:
    if not args.all and not args.target_source_path:
        raise SystemExit("pass --all or at least one --target-source-path")
    skill_root = resolve_skill_root(args.skill_root)
    payload = sync_out(
        skill_root=skill_root,
        target_source_paths=args.target_source_path,
        sync_all=args.all,
    )
    return print_payload(payload, args.json)


def main() -> int:
    parser = build_parser(cmd_registry, cmd_scan_collect, cmd_sync_out)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
