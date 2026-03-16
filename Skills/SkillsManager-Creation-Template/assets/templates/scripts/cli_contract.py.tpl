#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_ROOT / "DIRECTIVE_INDEX.json"


def emit(payload: dict[str, object], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(payload.get("status", "ok"))
    return 0


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(read_json(CONTRACT_PATH), args.json)


def cmd_directive(args: argparse.Namespace) -> int:
    index = read_json(DIRECTIVE_INDEX_PATH)
    topics = index.get("topics", {})
    if not isinstance(topics, dict) or args.topic not in topics:
        raise SystemExit(f"unknown topic: {args.topic}")
    entry = topics[args.topic]
    if not isinstance(entry, dict):
        raise SystemExit(f"invalid directive index for: {args.topic}")
    json_path = entry.get("json_path")
    if not isinstance(json_path, str):
        raise SystemExit(f"invalid directive json_path for: {args.topic}")
    return emit(read_json(RUNTIME_ROOT / json_path), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="{{skill_name}} toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
