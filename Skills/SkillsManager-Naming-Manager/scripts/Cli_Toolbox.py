#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from naming_manager_runtime import compile_reading_chain
from naming_manager_runtime import runtime_payload

SKILL_ROOT = Path(__file__).resolve().parents[1]


def _print_payload(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Naming-Manager toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("runtime-contract", "contract"):
        sub = subparsers.add_parser(name, help="Read the local runtime payload")
        sub.add_argument("--json", action="store_true")

    for name in ("read-path-context", "read-contract-context"):
        sub = subparsers.add_parser(name, help="Compile one local naming-governance chain into one context")
        sub.add_argument("--entry", required=True, help="Top-level entry key declared under SKILL.md section 2")
        sub.add_argument("--selection", default="", help="Comma-separated branch keys used when the chain hits a branch node")
        sub.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command in {"runtime-contract", "contract"}:
        return _print_payload(runtime_payload(), args.json)

    if args.command in {"read-path-context", "read-contract-context"}:
        selection = [item.strip() for item in args.selection.split(",") if item.strip()]
        return _print_payload(compile_reading_chain(SKILL_ROOT, args.entry, selection), args.json)

    raise ValueError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
