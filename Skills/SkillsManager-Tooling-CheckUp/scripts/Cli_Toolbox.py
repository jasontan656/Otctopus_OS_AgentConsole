#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import TypedDict, cast

import yaml

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
    path_dir_exists: bool
    skill_mode: str | None
    cli_entry_present: bool
    chain_reader_required: bool
    chain_reader_present: bool
    chain_reader_status: str | None
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
        return 0
    if "action" in payload:
        print(payload["action"])
        print(f"compliant: {payload['compliant']}")
        return 0
    print(payload["contract_name"])
    return 0


def _parse_frontmatter(markdown_path: Path) -> dict[str, object]:
    text = markdown_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}
    payload = yaml.safe_load(text[4:closing]) or {}
    return payload if isinstance(payload, dict) else {}


def _reading_chain(markdown_path: Path) -> list[dict[str, str]]:
    frontmatter = _parse_frontmatter(markdown_path)
    if markdown_path.name == "SKILL.md":
        metadata = frontmatter.get("metadata")
        doc_structure = metadata.get("doc_structure", {}) if isinstance(metadata, dict) else {}
        raw = doc_structure.get("reading_chain")
    else:
        raw = frontmatter.get("reading_chain")
    if not isinstance(raw, list):
        return []
    items: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            items.append({"key": key, "target": target, "hop": hop})
    return items


def _detect_cli_entry(scripts_dir: Path) -> Path | None:
    if not scripts_dir.is_dir():
        return None
    for name in ("Cli_Toolbox.py", "Cli_Toolbox.ts", "Cli_Toolbox.js"):
        candidate = scripts_dir / name
        if candidate.exists():
            return candidate
    return None


def _invoke_chain_reader(cli_path: Path, target_root: Path, entry: str, selection: list[str]) -> tuple[bool, dict[str, object] | None, str | None]:
    cmd = ["python3", str(cli_path), "read-path-context", "--entry", entry]
    if selection:
        cmd.extend(["--selection", ",".join(selection)])
    cmd.append("--json")
    completed = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=True,
        cwd=target_root,
    )
    if completed.returncode != 0:
        return False, None, "command_failed"
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return False, None, "invalid_json"
    status = payload.get("status")
    return True, payload if isinstance(payload, dict) else None, str(status) if isinstance(status, str) else None


def _run_chain_reader(cli_path: Path, target_root: Path) -> tuple[bool, str | None]:
    skill_md = target_root / "SKILL.md"
    root_chain = _reading_chain(skill_md)
    if not root_chain:
        return False, None
    entry = root_chain[0]["key"]
    selection: list[str] = []
    for _ in range(8):
        ok, payload, status = _invoke_chain_reader(cli_path, target_root, entry, selection)
        if not ok or payload is None or status is None:
            return False, status
        if status == "ok":
            required_fields = {"resolved_chain", "segments", "compiled_markdown"}
            return required_fields.issubset(payload.keys()), status
        if status != "branch_selection_required":
            return False, status
        available_next = payload.get("available_next")
        if not (isinstance(available_next, list) and available_next and isinstance(available_next[0], str)):
            return False, "branch_selection_required"
        selection.append(available_next[0])
    return False, "branch_selection_required"


def _audit_target_skill_root(target_root: Path) -> GovernAudit:
    skill_path = target_root / "SKILL.md"
    skill_frontmatter = _parse_frontmatter(skill_path)
    skill_mode = skill_frontmatter.get("skill_mode")
    if not isinstance(skill_mode, str):
        skill_mode = None

    scripts_dir = target_root / "scripts"
    path_dir = target_root / "path"
    scripts_dir_exists = scripts_dir.is_dir()
    path_dir_exists = path_dir.is_dir()
    cli_entry = _detect_cli_entry(scripts_dir)
    tooling_surface_detected = scripts_dir_exists
    chain_reader_required = scripts_dir_exists and path_dir_exists and skill_mode != "guide_only"

    if not tooling_surface_detected:
        return {
            "audit_mode": "no_tooling_surface_detected",
            "tooling_surface_detected": False,
            "scripts_dir_exists": False,
            "path_dir_exists": False,
            "skill_mode": skill_mode,
            "cli_entry_present": False,
            "chain_reader_required": False,
            "chain_reader_present": False,
            "chain_reader_status": None,
            "notes": [
                "no governed tooling surface was detected under the target skill root",
                "shape governance remains out of scope for SkillsManager-Tooling-CheckUp",
            ],
        }

    notes: list[str] = []
    chain_reader_present = False
    chain_reader_status: str | None = None

    if cli_entry is None:
        notes.append("scripts/ exists but no explicit Cli_Toolbox entry was detected")
    elif chain_reader_required:
        chain_reader_present, chain_reader_status = _run_chain_reader(cli_entry, target_root)
        if not chain_reader_present:
            notes.append("path-based tooling skill is missing a working read-path-context entry")

    return {
        "audit_mode": "tooling_surface_audit",
        "tooling_surface_detected": True,
        "scripts_dir_exists": scripts_dir_exists,
        "path_dir_exists": path_dir_exists,
        "skill_mode": skill_mode,
        "cli_entry_present": cli_entry is not None,
        "chain_reader_required": chain_reader_required,
        "chain_reader_present": chain_reader_present,
        "chain_reader_status": chain_reader_status,
        "notes": notes,
    }


def _build_recommended_actions(audit: GovernAudit) -> list[str]:
    if not audit["tooling_surface_detected"]:
        return ["no governed tooling surface was detected; stop and do not reinterpret this target as a shape-governance problem"]
    actions: list[str] = []
    if audit["scripts_dir_exists"] and not audit["cli_entry_present"]:
        actions.append("review scripts/ and expose one explicit Cli_Toolbox entry if this target intends to ship a governed CLI surface")
    if audit["chain_reader_required"] and not audit["chain_reader_present"]:
        actions.append("add a working read-path-context command so the target can compile one governed reading chain into JSON context output")
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
        print(json.dumps({"status": "error", "error": "unknown_directive_topic", "topic": args.topic}, ensure_ascii=False, indent=2))
        return 1
    return emit(payload, args.json)


def cmd_govern_target(args: argparse.Namespace) -> int:
    target_root = Path(args.target_skill_root).expanduser().resolve()
    skill_path = target_root / "SKILL.md"
    if not target_root.exists() or not target_root.is_dir():
        print(json.dumps({"status": "error", "error": "target_skill_root_not_found", "target_skill_root": str(target_root)}, ensure_ascii=False, indent=2))
        return 1
    if not skill_path.exists():
        print(json.dumps({"status": "error", "error": "target_skill_root_missing_skill_md", "target_skill_root": str(target_root)}, ensure_ascii=False, indent=2))
        return 1

    governance_contract = cast(DirectivePayload, read_json(TOOLING_ENTRY_GUIDE_PATH))
    audit = _audit_target_skill_root(target_root)
    compliant = (not audit["tooling_surface_detected"]) or (
        audit["cli_entry_present"] and (not audit["chain_reader_required"] or audit["chain_reader_present"])
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
