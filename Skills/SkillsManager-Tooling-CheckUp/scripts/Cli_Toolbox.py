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
TARGET_GOVERNANCE_CONTRACT_PATH = RUNTIME_CONTRACTS_ROOT / "TARGET_SHAPE_GOVERNANCE_GUIDE.json"
RUNTIME_DOC_KEYWORDS = ("CONTRACT", "WORKFLOW", "INSTRUCTION", "GUIDE")


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
    runtime_contract_dir_exists: bool
    facade_cli_first: bool
    agent_prompt_cli_first: bool
    paired_runtime_assets: list[str]
    missing_human_mirrors: list[str]
    missing_json_payloads: list[str]
    legacy_markdown_only_assets: list[str]
    orphan_json_assets: list[str]
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


def _looks_like_runtime_doc(path: Path) -> bool:
    upper_name = path.name.upper()
    return any(keyword in upper_name for keyword in RUNTIME_DOC_KEYWORDS)


def _is_cli_first_text(text: str) -> bool:
    return (
        "Cli_Toolbox.py" in text
        and "--json" in text
        and (
            "contract" in text
            or "directive" in text
            or "govern-target" in text
        )
    )


def _expected_json_for_human(human_path: Path) -> Path:
    return human_path.with_name(human_path.name.removesuffix("_human.md") + ".json")


def _expected_human_for_json(json_path: Path) -> Path:
    return json_path.with_name(f"{json_path.stem}_human.md")


def _audit_target_skill_root(target_root: Path) -> GovernAudit:
    runtime_contract_dir = target_root / "references" / "runtime_contracts"
    paired_runtime_assets: list[str] = []
    missing_human_mirrors: list[str] = []
    missing_json_payloads: list[str] = []
    legacy_markdown_only_assets: list[str] = []
    orphan_json_assets: list[str] = []
    notes: list[str] = []

    if runtime_contract_dir.exists():
        for json_path in sorted(runtime_contract_dir.glob("*.json")):
            if json_path.name == "DIRECTIVE_INDEX.json":
                continue
            human_path = _expected_human_for_json(json_path)
            if human_path.exists():
                paired_runtime_assets.append(str(json_path.relative_to(target_root)))
            else:
                missing_human_mirrors.append(str(json_path.relative_to(target_root)))
        for human_path in sorted(runtime_contract_dir.glob("*_human.md")):
            json_path = _expected_json_for_human(human_path)
            if not json_path.exists():
                missing_json_payloads.append(str(human_path.relative_to(target_root)))
    else:
        notes.append("target skill has no references/runtime_contracts directory")

    skill_path = target_root / "SKILL.md"
    facade_cli_first = skill_path.exists() and _is_cli_first_text(skill_path.read_text(encoding="utf-8"))
    if not facade_cli_first:
        notes.append("skill facade does not present a clear CLI-first runtime entry")

    agent_path = target_root / "agents" / "openai.yaml"
    agent_prompt_cli_first = agent_path.exists() and _is_cli_first_text(agent_path.read_text(encoding="utf-8"))
    if not agent_prompt_cli_first:
        notes.append("agent default prompt does not present a clear CLI-first runtime entry")

    references_root = target_root / "references"
    for md_path in sorted(references_root.rglob("*.md")) if references_root.exists() else []:
        if md_path.name == "SKILL.md" or md_path.name.endswith("_human.md"):
            continue
        if "runtime_contracts" in md_path.parts:
            continue
        if md_path.parts[-3:-1] == ("tooling", "development") or "modules" in md_path.parts:
            continue
        if _looks_like_runtime_doc(md_path):
            legacy_markdown_only_assets.append(str(md_path.relative_to(target_root)))

    for json_path in sorted(references_root.rglob("*.json")) if references_root.exists() else []:
        if "runtime_contracts" in json_path.parts:
            continue
        if json_path.parts[-3:-1] == ("tooling", "development") or "modules" in json_path.parts:
            continue
        if _looks_like_runtime_doc(json_path):
            orphan_json_assets.append(str(json_path.relative_to(target_root)))

    return {
        "runtime_contract_dir_exists": runtime_contract_dir.exists(),
        "facade_cli_first": facade_cli_first,
        "agent_prompt_cli_first": agent_prompt_cli_first,
        "paired_runtime_assets": paired_runtime_assets,
        "missing_human_mirrors": missing_human_mirrors,
        "missing_json_payloads": missing_json_payloads,
        "legacy_markdown_only_assets": legacy_markdown_only_assets,
        "orphan_json_assets": orphan_json_assets,
        "notes": notes,
    }


def _build_recommended_actions(audit: GovernAudit) -> list[str]:
    actions: list[str] = []
    if not audit["runtime_contract_dir_exists"]:
        actions.append("create references/runtime_contracts and move runtime-facing contract assets there")
    if not audit["facade_cli_first"]:
        actions.append("rewrite SKILL.md so the model enters through CLI JSON instead of markdown path chains")
    if not audit["agent_prompt_cli_first"]:
        actions.append("rewrite agents/openai.yaml default_prompt so it points to CLI JSON entry commands")
    if audit["missing_human_mirrors"]:
        actions.append("create *_human.md mirrors for runtime JSON assets that currently lack them")
    if audit["missing_json_payloads"]:
        actions.append("create same-name .json payload files for *_human.md runtime assets that currently lack them")
    if audit["legacy_markdown_only_assets"]:
        actions.append("migrate legacy markdown-only contract/workflow/instruction/guide assets into runtime_contracts dual-file form")
    if audit["orphan_json_assets"]:
        actions.append("review JSON runtime assets outside runtime_contracts and either pair them with *_human.md or relocate them")
    if not actions:
        actions.append("target skill already satisfies the governed dual-file and CLI-first shape")
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

    governance_contract = cast(DirectivePayload, read_json(TARGET_GOVERNANCE_CONTRACT_PATH))
    audit = _audit_target_skill_root(target_root)
    compliant = (
        audit["runtime_contract_dir_exists"]
        and audit["facade_cli_first"]
        and audit["agent_prompt_cli_first"]
        and not audit["missing_human_mirrors"]
        and not audit["missing_json_payloads"]
        and not audit["legacy_markdown_only_assets"]
        and not audit["orphan_json_assets"]
    )
    payload: GovernTargetPayload = {
        "status": "ok",
        "action": "govern_target_skill_shape",
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
