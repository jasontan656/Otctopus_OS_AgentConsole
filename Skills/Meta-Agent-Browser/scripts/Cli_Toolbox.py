#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
PRODUCT_ROOT = SKILL_ROOT.parents[1]
WORKSPACE_ROOT = PRODUCT_ROOT.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_CONTRACTS_ROOT / "DIRECTIVE_INDEX.json"
SKILL_NAME = SKILL_ROOT.name
RUNTIME_DIR = WORKSPACE_ROOT / "Codex_Skill_Runtime" / SKILL_NAME
RESULT_DIR = WORKSPACE_ROOT / "Codex_Skills_Result" / SKILL_NAME

PLACEHOLDERS = {
    "__SKILL_NAME__": SKILL_NAME,
    "__SKILL_ROOT__": str(SKILL_ROOT),
    "__PRODUCT_ROOT__": str(PRODUCT_ROOT),
    "__WORKSPACE_ROOT__": str(WORKSPACE_ROOT),
    "__RUNTIME_DIR__": str(RUNTIME_DIR),
    "__RESULT_DIR__": str(RESULT_DIR),
}


def _replace_placeholders(value: Any) -> Any:
    if isinstance(value, str):
        rendered = value
        for placeholder, resolved in PLACEHOLDERS.items():
            rendered = rendered.replace(placeholder, resolved)
        return rendered
    if isinstance(value, list):
        return [_replace_placeholders(item) for item in value]
    if isinstance(value, dict):
        return {key: _replace_placeholders(item) for key, item in value.items()}
    return value


def _read_json_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return _replace_placeholders(payload)


def _read_directive_index() -> dict[str, dict[str, str]]:
    payload = json.loads(DIRECTIVE_INDEX_PATH.read_text(encoding="utf-8"))
    return payload["topics"]


def _emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if "directive_name" in payload:
        print(payload["directive_name"])
        print(f"purpose: {payload['purpose']}")
        for section in ("instruction", "workflow", "rules"):
            values = payload.get(section, [])
            if not values:
                continue
            print(f"{section}:")
            for item in values:
                print(f"- {item}")
        return 0

    if "resolved_paths" in payload:
        for key, value in payload["resolved_paths"].items():
            print(f"{key}: {value}")
        return 0

    print(payload["contract_name"])
    print(f"version: {payload['contract_version']}")
    print("tool_entry:")
    for name, command in payload["tool_entry"]["commands"].items():
        print(f"- {name}: {command}")
    print("directive_topics:")
    for item in payload["directive_topics"]:
        print(f"- {item['topic']}: {item['doc_kind']}")
    return 0


def _command_contract(args: argparse.Namespace) -> int:
    return _emit(_read_json_payload(CONTRACT_PATH), args.json)


def _command_directive(args: argparse.Namespace) -> int:
    directive_index = _read_directive_index()
    entry = directive_index.get(args.topic)
    if entry is None:
        available = ", ".join(sorted(directive_index))
        raise SystemExit(f"Unknown directive topic: {args.topic}. Available: {available}")
    payload = _read_json_payload(RUNTIME_CONTRACTS_ROOT / entry["json_path"])
    return _emit(payload, args.json)


def _command_paths(args: argparse.Namespace) -> int:
    payload = {
        "skill_name": SKILL_NAME,
        "resolved_paths": {
            "skill_root": str(SKILL_ROOT),
            "product_root": str(PRODUCT_ROOT),
            "workspace_root": str(WORKSPACE_ROOT),
            "runtime_dir": str(RUNTIME_DIR),
            "result_dir": str(RESULT_DIR),
        },
        "environment_variables": {
            "META_AGENT_BROWSER_RUNTIME_DIR": str(RUNTIME_DIR),
            "META_AGENT_BROWSER_RESULT_DIR": str(RESULT_DIR),
        },
    }
    return _emit(payload, args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Meta-Agent-Browser CLI toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract_parser = subparsers.add_parser("contract", help="Emit the runtime contract")
    contract_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    contract_parser.set_defaults(func=_command_contract)

    directive_parser = subparsers.add_parser("directive", help="Emit a directive payload")
    directive_parser.add_argument("--topic", required=True, help="Directive topic name")
    directive_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    directive_parser.set_defaults(func=_command_directive)

    paths_parser = subparsers.add_parser("paths", help="Resolve governed skill paths")
    paths_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    paths_parser.set_defaults(func=_command_paths)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
