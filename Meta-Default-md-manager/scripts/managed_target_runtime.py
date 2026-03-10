from __future__ import annotations

import json
from pathlib import Path

from managed_agents_text import is_agents_target_kind
from managed_paths import legacy_root_slugs, managed_root
from managed_registry import load_registry

AGENT_AUDIT_FILENAME = "AGENT_AUDIT.md"
README_AUDIT_FILENAME = "README_AUDIT.md"
MIRROR_CLI = "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py"


def target_contract_root(skill_root: Path) -> Path:
    return managed_root(skill_root) / "runtime_rules"


def _runtime_json_filename(target_kind: str) -> str:
    stem = Path(target_kind).stem
    return f"{stem}.runtime.json"


def _audit_filename(target_kind: str) -> str:
    if target_kind == "AGENTS.md":
        return AGENT_AUDIT_FILENAME
    if target_kind == "README.md":
        return README_AUDIT_FILENAME
    stem = Path(target_kind).stem.upper()
    return f"{stem}_AUDIT.md"


def legacy_runtime_json_path(skill_root: Path, managed_rel_path: str, target_kind: str) -> Path:
    return target_contract_root(skill_root) / Path(managed_rel_path).parent / _runtime_json_filename(target_kind)


def legacy_audit_md_path(skill_root: Path, managed_rel_path: str, target_kind: str) -> Path:
    return target_contract_root(skill_root) / Path(managed_rel_path).parent / _audit_filename(target_kind)


def runtime_json_path(skill_root: Path, entry: dict[str, str]) -> Path:
    if is_agents_target_kind(entry["target_kind"]):
        return Path(entry["machine_path"])
    return legacy_runtime_json_path(skill_root, entry["managed_rel_path"], entry["target_kind"])


def audit_md_path(skill_root: Path, entry: dict[str, str]) -> Path:
    if is_agents_target_kind(entry["target_kind"]):
        return Path(entry["audit_md_path"])
    return legacy_audit_md_path(skill_root, entry["managed_rel_path"], entry["target_kind"])


def _source_rel(entry: dict[str, str]) -> str:
    source_root = Path(entry["source_root"])
    source_path = Path(entry["source_path"])
    return source_path.relative_to(source_root).as_posix()


def _peer_doc(entry: dict[str, str]) -> dict[str, str]:
    source_path = Path(entry["source_path"])
    if entry["target_kind"] == "AGENTS.md":
        peer = source_path.with_name("README.md")
        return {
            "path": str(peer),
            "relation": "same_level_summary",
            "read_policy": "optional_then_required_on_write_if_exists" if peer.exists() else "not_available",
        }
    if entry["target_kind"] == "README.md":
        peer = source_path.with_name("AGENTS.md")
        return {
            "path": str(peer),
            "relation": "same_level_runtime_entry",
            "read_policy": "required_first_if_exists" if peer.exists() else "not_available",
        }
    return {
        "path": "",
        "relation": "none",
        "read_policy": "not_applicable",
    }


def _turn_contract(source_rel: str, target_kind: str) -> dict[str, object]:
    if source_rel == "AGENTS.md" and target_kind == "AGENTS.md":
        return {
            "status": "enforced",
            "turn_start": [
                "validate /home/jasontan656/AI_Projects/AGENTS.md exists",
                "print TURN_START guardrails",
                "print ROUTE guardrails",
                "choose READ_EXEC or WRITE_EXEC by write intent",
            ],
            "turn_end": [
                "print TURN_END guardrails",
            ],
        }
    if source_rel == "Codex_Skills_Mirror/AGENTS.md" and target_kind == "AGENTS.md":
        return {
            "status": "enforced",
            "turn_start": [
                "use the returned target contract JSON as the runtime rule source",
                "if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start",
            ],
            "turn_end": [
                "run Constitution lint on the concrete Codex_Skills_Mirror target root",
                "if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn",
            ],
        }
    return {
        "status": "n_a",
        "turn_start": ["N/A"],
        "turn_end": ["N/A"],
    }


def build_target_contract(entry: dict[str, str], *, skill_root: Path) -> dict[str, object]:
    source_rel = _source_rel(entry)
    source_path = Path(entry["source_path"])
    command = (
        f"python3 {MIRROR_CLI} target-contract "
        f'--source-path "{entry["source_path"]}" --json'
    )
    target_kind = entry["target_kind"]
    file_kind = "agents" if target_kind == "AGENTS.md" else "readme"
    contract = {
        "schema_version": 1,
        "owner_skill": "Meta-Default-md-manager",
        "managed_branch": "default_docs",
        "rule_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "human_audit_source": "audit_markdown_only",
            "model_must_not_read_markdown_for_runtime_guidance": True,
        },
        "target": {
            "source_root": entry["source_root"],
            "source_path": entry["source_path"],
            "source_relative_path": source_rel,
            "file_kind": file_kind,
            "target_kind": target_kind,
            "peer_path": _peer_doc(entry)["path"],
            "managed_rel_path": entry["managed_rel_path"],
            "managed_dir": entry["managed_dir"],
        },
        "peer_doc": _peer_doc(entry),
        "runtime_entry": {
            "cli": command,
            "audit_md_path": str(audit_md_path(skill_root, entry)),
            "runtime_json_path": str(runtime_json_path(skill_root, entry)),
        },
        "turn_contract": _turn_contract(source_rel, target_kind),
        "routing": {
            "document_role": "runtime_entry" if target_kind == "AGENTS.md" else "human_summary",
            "default_next_hop": "use the target-contract JSON to decide peer reads and manager commands",
            "rules": [
                "use Meta-Default-md-manager CLI JSON as the runtime rule source",
                "README-like files remain human summaries unless a peer AGENTS contract says otherwise",
                "machine-readable runtime rules must stay in skill-managed JSON and CLI output",
            ],
        },
        "update_boundary": [
            "managed targets are owned by Meta-Default-md-manager",
            "external AGENTS.md should remain a thin runtime entry",
            "skill-managed JSON and CLI output are the runtime source of truth",
        ],
    }
    if is_agents_target_kind(target_kind):
        contract["target"]["human_path"] = entry["human_path"]
        contract["target"]["machine_path"] = entry["machine_path"]
    else:
        contract["target"]["managed_path"] = entry["managed_path"]
    if source_path.name != "AGENTS.md":
        contract["update_boundary"][1] = "external README-like files remain human-readable summaries"
    return contract


def render_external_agents(entry: dict[str, str]) -> str:
    command = (
        f"python3 {MIRROR_CLI} "
        f'target-contract --source-path "{entry["source_path"]}" --json'
    )
    turn_contract = _turn_contract(_source_rel(entry), entry["target_kind"])
    turn_start = turn_contract["turn_start"]
    turn_end = turn_contract["turn_end"]
    lines = [
        "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]",
        "",
        "`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.",
        "",
        "[TURN START - MANDATORY]",
        "",
        "1. Load Target Contract",
        "- Must run this command before following any path-specific rule:",
        f"- `{command}`",
        "",
        "2. TURN_START Contract",
    ]
    lines.extend([f"- {item}" for item in turn_start])
    lines.extend(
        [
        "",
        "3. Peer Document Gate",
        "- See the returned `peer_doc` object to decide whether the same-level peer file exists and whether it must be read.",
        "",
        "[EXECUTION - MANDATORY]",
        "",
        "4. Runtime Rule Source",
        "- The CLI JSON output is the runtime rule source for this path.",
        "- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.",
        "",
        "5. Managed Boundary",
        f"- Current target kind: `{entry['target_kind']}`.",
        "- `AGENTS.md` should remain a thin runtime entry; concrete routing/update rules live in the returned JSON contract.",
        "",
        "[TURN END - MANDATORY]",
        "",
        "6. TURN_END Contract",
        ]
    )
    lines.extend([f"- {item}" for item in turn_end])
    lines.append("")
    return "\n".join(lines)


def render_audit_markdown(contract: dict[str, object]) -> str:
    target = contract["target"]
    peer_doc = contract["peer_doc"]
    runtime_entry = contract["runtime_entry"]
    turn_contract = contract["turn_contract"]
    lines = [
        "# Target Rule Audit",
        "",
        "> Human audit copy generated from the skill-managed target runtime JSON.",
        "> Runtime models must call the CLI listed below instead of reading this markdown.",
        "",
        "## Target",
        f"- source_path: `{target['source_path']}`",
        f"- target_kind: `{target['target_kind']}`",
        f"- managed_rel_path: `{target['managed_rel_path']}`",
        "",
        "## Runtime Entry",
        f"- cli: `{runtime_entry['cli']}`",
        f"- runtime_json_path: `{runtime_entry['runtime_json_path']}`",
        "",
        "## Peer Doc",
        f"- path: `{peer_doc['path']}`",
        f"- read_policy: `{peer_doc['read_policy']}`",
        "",
        "## Turn Contract",
        f"- status: `{turn_contract['status']}`",
        "- turn_start:",
    ]
    lines.extend([f"  - {item}" for item in turn_contract["turn_start"]])
    lines.append("- turn_end:")
    lines.extend([f"  - {item}" for item in turn_contract["turn_end"]])
    lines.append("")
    return "\n".join(lines)


def _prune_runtime_rules(skill_root: Path, entries: list[dict[str, str]]) -> None:
    runtime_root = target_contract_root(skill_root)
    if not runtime_root.exists():
        return

    live_rel_paths: set[str] = set()
    source_roots: set[Path] = set()
    for entry in entries:
        source_roots.add(Path(entry["source_root"]))
        for target in (runtime_json_path(skill_root, entry), audit_md_path(skill_root, entry)):
            if target.is_relative_to(runtime_root):
                live_rel_paths.add(target.relative_to(runtime_root).as_posix())

    for source_root in source_roots:
        for slug in legacy_root_slugs(source_root):
            namespace_root = runtime_root / slug
            if not namespace_root.exists():
                continue
            for target in sorted(namespace_root.rglob("*")):
                if not target.is_file():
                    continue
                rel_path = target.relative_to(runtime_root).as_posix()
                if rel_path in live_rel_paths:
                    continue
                target.unlink()
            for candidate in sorted(namespace_root.rglob("*"), reverse=True):
                if candidate.is_dir() and not any(candidate.iterdir()):
                    candidate.rmdir()
            if namespace_root.exists() and not any(namespace_root.iterdir()):
                namespace_root.rmdir()


def write_target_contract_assets(skill_root: Path, entries: list[dict[str, str]]) -> list[str]:
    written: list[str] = []
    for entry in entries:
        contract = build_target_contract(entry, skill_root=skill_root)
        json_path = runtime_json_path(skill_root, entry)
        md_path = audit_md_path(skill_root, entry)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md_path.write_text(render_audit_markdown(contract), encoding="utf-8")
        if is_agents_target_kind(entry["target_kind"]):
            for legacy in (
                legacy_runtime_json_path(skill_root, entry["managed_rel_path"], entry["target_kind"]),
                legacy_audit_md_path(skill_root, entry["managed_rel_path"], entry["target_kind"]),
            ):
                if legacy.exists():
                    legacy.unlink()
        written.extend([str(json_path), str(md_path)])
    _prune_runtime_rules(skill_root, entries)
    return written


def load_target_contract(skill_root: Path, source_path: str) -> dict[str, object]:
    payload = load_registry(skill_root, require_existing=True)
    for entry in payload.get("entries", []):
        if entry["source_path"] == str(Path(source_path).expanduser().resolve()):
            if is_agents_target_kind(entry["target_kind"]):
                machine_path = Path(entry.get("machine_path", ""))
                if machine_path.exists():
                    return json.loads(machine_path.read_text(encoding="utf-8"))
            return build_target_contract(entry, skill_root=skill_root)
    raise ValueError(f"target not found in registry: {source_path}")
