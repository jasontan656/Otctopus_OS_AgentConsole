#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import TypedDict, cast


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
RUNTIME_CONTRACTS_ROOT = SKILL_ROOT / "references" / "runtime_contracts"
CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "SKILL_RUNTIME_CONTRACT.json"
DIRECTIVE_INDEX_PATH = RUNTIME_CONTRACTS_ROOT / "DIRECTIVE_INDEX.json"

MANAGED_ROOT = Path("/home/jasontan656/AI_Projects/Human_Work_Zone")
MANAGED_ZONES = {
    "open_source_projects": MANAGED_ROOT / "Open_Source_Projects",
    "backup_management": MANAGED_ROOT / "Backup_Management",
    "open_source_project_analysis": MANAGED_ROOT / "Open_Source_Project_Analysis",
    "books_and_readings": MANAGED_ROOT / "Books_and_Readings",
    "temporary_projects": MANAGED_ROOT / "Temporary_Projects",
    "company_documents": MANAGED_ROOT / "Company_Documents",
    "external_research_reports": MANAGED_ROOT / "External_Research_Reports",
}


class ToolEntry(TypedDict):
    script: str
    commands: dict[str, str]


class DirectiveTopic(TypedDict):
    topic: str
    doc_kind: str
    use_when: str


class ContractPayload(TypedDict):
    contract_name: str
    contract_version: str
    skill_name: str
    runtime_source_policy: dict[str, object]
    tool_entry: ToolEntry
    must_use_sequence: list[str]
    directive_topics: list[DirectiveTopic]
    managed_root: str
    hard_constraints: list[str]


class DirectivePayload(TypedDict):
    directive_name: str
    directive_version: str
    doc_kind: str
    topic: str
    purpose: str
    instruction: list[str]
    workflow: list[str]
    rules: list[str]


class PathsPayload(TypedDict):
    managed_root: str
    zones: dict[str, str]


Payload = ContractPayload | DirectivePayload | PathsPayload


class DirectiveIndexEntry(TypedDict):
    doc_kind: str
    json_path: str
    human_path: str


class DirectiveIndex(TypedDict):
    topics: dict[str, DirectiveIndexEntry]


def read_json(path: Path) -> Payload:
    return cast(Payload, json.loads(path.read_text(encoding="utf-8")))


def read_directive_index(path: Path) -> DirectiveIndex:
    return cast(DirectiveIndex, json.loads(path.read_text(encoding="utf-8")))


def emit(payload: Payload, as_json: bool) -> int:
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
    if "contract_name" in payload:
        print(payload["contract_name"])
        print(f"version: {payload['contract_version']}")
        print("tool_entry:")
        for name, command in payload["tool_entry"]["commands"].items():
            print(f"- {name}: {command}")
        return 0
    print("managed_root:")
    print(payload["managed_root"])
    print("zones:")
    for name, path in payload["zones"].items():
        print(f"- {name}: {path}")
    return 0


def build_paths_payload() -> PathsPayload:
    return {
        "managed_root": str(MANAGED_ROOT),
        "zones": {name: str(path) for name, path in MANAGED_ZONES.items()},
    }


def _resolve_directive_path(topic: str) -> Path:
    directive = read_directive_index(DIRECTIVE_INDEX_PATH).get("topics", {}).get(topic)
    if not directive:
        raise KeyError(topic)
    return RUNTIME_CONTRACTS_ROOT / directive["json_path"]


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(read_json(CONTRACT_PATH), args.json)


def cmd_directive(args: argparse.Namespace) -> int:
    try:
        payload = read_json(_resolve_directive_path(args.topic))
    except KeyError:
        available_topics = ", ".join(sorted(read_directive_index(DIRECTIVE_INDEX_PATH)["topics"].keys()))
        raise SystemExit(f"unknown topic: {args.topic}. available topics: {available_topics}") from None
    return emit(payload, args.json)


def cmd_paths(args: argparse.Namespace) -> int:
    return emit(build_paths_payload(), args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI-first runtime contract entry for Functional-HumenWorkZone-Manager."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    paths = subparsers.add_parser("paths")
    paths.add_argument("--json", action="store_true")
    paths.set_defaults(func=cmd_paths)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
