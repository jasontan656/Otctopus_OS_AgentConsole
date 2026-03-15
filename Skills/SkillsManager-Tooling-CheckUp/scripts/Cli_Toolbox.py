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
TOOLING_ENTRY_GUIDE_PATH = RUNTIME_CONTRACTS_ROOT / "TOOLING_ENTRY_GUIDE.json"
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
    hard_constraints: list[str]
    target_skill_handoff: list[str]


class DirectivePayload(TypedDict):
    directive_name: str
    directive_version: str
    doc_kind: str
    topic: str
    purpose: str
    instruction: list[str]
    workflow: list[str]
    rules: list[str]


class GovernAudit(TypedDict):
    audit_mode: str
    tooling_surface_detected: bool
    scripts_dir_exists: bool
    cli_entry_present: bool
    notes: list[str]


class GovernTargetPayload(TypedDict):
    status: str
    action: str
    target_skill_root: str
    governance_contract: DirectivePayload
    audit: GovernAudit
    compliant: bool
    recommended_actions: list[str]


Payload = ContractPayload | DirectivePayload | GovernTargetPayload


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
    if "action" in payload:
        print(payload["action"])
        print(f"target_skill_root: {payload['target_skill_root']}")
        print(f"compliant: {payload['compliant']}")
        print("recommended_actions:")
        for item in payload["recommended_actions"]:
            print(f"- {item}")
        return 0
    print(payload["contract_name"])
    print(f"version: {payload['contract_version']}")
    if payload.get("tool_entry"):
        print("tool_entry:")
        for name, command in payload["tool_entry"]["commands"].items():
            print(f"- {name}: {command}")
    if payload.get("directive_topics"):
        print("directive_topics:")
        for item in payload["directive_topics"]:
            print(f"- {item['topic']}: {item['doc_kind']}")
    return 0


def _detect_cli_entry(scripts_dir: Path) -> bool:
    if not scripts_dir.is_dir():
        return False
    patterns = ("Cli_Toolbox.py", "Cli_Toolbox.ts", "Cli_Toolbox.js")
    return any((scripts_dir / name).exists() for name in patterns)


def _audit_target_skill_root(target_root: Path) -> GovernAudit:
    scripts_dir = target_root / "scripts"
    scripts_dir_exists = scripts_dir.is_dir()
    cli_entry_present = _detect_cli_entry(scripts_dir)
    tooling_surface_detected = scripts_dir_exists

    if not tooling_surface_detected:
        return {
            "audit_mode": "no_tooling_surface_detected",
            "tooling_surface_detected": False,
            "scripts_dir_exists": False,
            "cli_entry_present": False,
            "notes": [
                "no governed tooling surface was detected under the target skill root",
                "shape governance remains out of scope for SkillsManager-Tooling-CheckUp",
            ],
        }

    notes: list[str] = []

    if scripts_dir_exists and not cli_entry_present:
        notes.append("scripts/ exists but no explicit Cli_Toolbox entry was detected")

    return {
        "audit_mode": "tooling_surface_audit",
        "tooling_surface_detected": True,
        "scripts_dir_exists": scripts_dir_exists,
        "cli_entry_present": cli_entry_present,
        "notes": notes,
    }


def _build_recommended_actions(audit: GovernAudit) -> list[str]:
    if not audit["tooling_surface_detected"]:
        return [
            "no governed tooling surface was detected; stop and do not reinterpret this target as a shape-governance problem"
        ]
    actions: list[str] = []
    if audit["scripts_dir_exists"] and not audit["cli_entry_present"]:
        actions.append("review scripts/ and expose one explicit Cli_Toolbox entry if this target intends to ship a governed CLI surface")
    if not actions:
        actions.append("target skill already satisfies the governed tooling runtime surface")
    return actions


def cmd_contract(args: argparse.Namespace) -> int:
    return emit(read_json(CONTRACT_PATH), args.json)


def _resolve_directive_path(topic: str) -> Path:
    index = read_directive_index(DIRECTIVE_INDEX_PATH)
    directive = index.get("topics", {}).get(topic)
    if not directive:
        raise KeyError(topic)
    return RUNTIME_CONTRACTS_ROOT / directive["json_path"]


def cmd_directive(args: argparse.Namespace) -> int:
    try:
        payload = read_json(_resolve_directive_path(args.topic))
    except KeyError:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "unknown_directive_topic",
                    "topic": args.topic,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    return emit(payload, args.json)


def cmd_govern_target(args: argparse.Namespace) -> int:
    target_root = Path(args.target_skill_root).expanduser().resolve()
    skill_path = target_root / "SKILL.md"
    if not target_root.exists() or not target_root.is_dir():
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "target_skill_root_not_found",
                    "target_skill_root": str(target_root),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    if not skill_path.exists():
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "target_skill_root_missing_skill_md",
                    "target_skill_root": str(target_root),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    governance_contract = cast(DirectivePayload, read_json(TOOLING_ENTRY_GUIDE_PATH))
    audit = _audit_target_skill_root(target_root)
    compliant = (not audit["tooling_surface_detected"]) or (
        audit["cli_entry_present"]
    )
    payload: GovernTargetPayload = {
        "status": "ok",
        "action": "govern_target_skill_tooling",
        "target_skill_root": str(target_root),
        "governance_contract": governance_contract,
        "audit": audit,
        "compliant": compliant,
        "recommended_actions": _build_recommended_actions(audit),
    }
    return emit(payload, args.json)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SkillsManager-Tooling-CheckUp unified toolbox")
    subparsers = parser.add_subparsers(dest="command", required=True)

    contract = subparsers.add_parser("contract")
    contract.add_argument("--json", action="store_true")
    contract.set_defaults(func=cmd_contract)

    directive = subparsers.add_parser("directive")
    directive.add_argument("--topic", required=True)
    directive.add_argument("--json", action="store_true")
    directive.set_defaults(func=cmd_directive)

    govern_target = subparsers.add_parser("govern-target")
    govern_target.add_argument("--target-skill-root", required=True)
    govern_target.add_argument("--json", action="store_true")
    govern_target.set_defaults(func=cmd_govern_target)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
