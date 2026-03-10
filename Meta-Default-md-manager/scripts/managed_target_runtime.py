from __future__ import annotations

import json
from pathlib import Path

from managed_agents_text import compose_managed_agents, extract_part_a, is_agents_target_kind
from managed_paths import legacy_root_slugs, managed_root
from managed_registry import load_registry

AGENT_AUDIT_FILENAME = "AGENT_AUDIT.md"
README_AUDIT_FILENAME = "README_AUDIT.md"
MIRROR_CLI = "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py"

BASE_RUNTIME_SOURCE_POLICY = {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": True,
    "path_metadata_is_not_action_guidance": True,
}

DEFAULT_META_SKILL_ORDER = [
    "$Meta-prompt-write (strengthen user intent and understand the real need)",
    "$Meta-mindchain (think from the architecture level and reject one-sided thinking)",
    "$Meta-reasoningchain (project the future shape to align the target state)",
    "$Meta-keyword-first-edit (prefer delete > replace > add when editing)",
    "$Meta-refactor-behavior-preserving (applicable only when refactor is needed)",
    "$Meta-Agent-Browser (applicable only when the task is frontend or browser-related)",
]

ROOT_AGENTS_PAYLOAD = {
    "entry_role": "workspace_root_runtime_entry",
    "runtime_source_policy": BASE_RUNTIME_SOURCE_POLICY,
    "default_meta_skill_order": DEFAULT_META_SKILL_ORDER,
    "turn_start_actions": [
        "validate root AGENTS exists",
        "classify the turn as READ_EXEC or WRITE_EXEC",
        "apply the default meta sequence before concrete execution",
    ],
    "runtime_constraints": [
        "treat CLI JSON as the primary runtime rule source",
        "do not use audit markdown as the primary execution guide",
        "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
        "when a concrete repo path becomes active, load that repo-local contract before repo-specific write, lint, or Git actions",
    ],
    "execution_modes": {
        "READ_EXEC": {
            "goal": "answer, inspect, classify, or route without changing files",
            "default_actions": [
                "prefer direct CLI contract output over opening markdown rule files",
                "open extra files only when the direct contract still leaves a real gap",
            ],
        },
        "WRITE_EXEC": {
            "goal": "edit files or trigger manager-owned write flows",
            "default_actions": [
                "apply the default meta sequence before editing",
                "state the intended write scope before editing",
                "edit the minimal correct scope that matches the user intent",
                "do not trigger Git automation unless the active repo-local contract or the user explicitly requires it",
            ],
        },
    },
    "repo_local_contract_handoff": [
        "if work enters a repo with its own AGENTS runtime entry, load that repo-local target-contract before following repo-specific rules",
        "repo-local contract may add stricter lint, delivery, or Git rules for that repo only",
        "when repo-local and workspace-root rules overlap, keep the workspace-root boundary and add the repo-local concrete duties",
    ],
    "forbidden_primary_runtime_pattern": [
        "Do not treat audit markdown paths as the main runtime instructions.",
        "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
        "Do not emit only path metadata when the real need is direct action guidance.",
    ],
    "turn_end_actions": [
        "print TURN_END guardrails",
        "defer repo-specific lint or Git duties to the concrete repo-local contract when applicable",
    ],
}


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
        return Path(entry["human_path"])
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


def _deep_copy_json(payload: dict[str, object]) -> dict[str, object]:
    return json.loads(json.dumps(payload, ensure_ascii=False))


def _peer_summary_policy(entry: dict[str, str]) -> dict[str, object]:
    peer_doc = _peer_doc(entry)
    available = peer_doc["read_policy"] != "not_available"
    if available:
        guidance = "same-level README.md is a human summary; read it only when the current task needs that summary"
    else:
        guidance = "same-level README.md is not available for this target"
    return {
        "available": available,
        "relation": peer_doc["relation"],
        "read_policy": peer_doc["read_policy"],
        "guidance": guidance,
    }


def build_agents_payload(entry: dict[str, str]) -> dict[str, object]:
    source_rel = _source_rel(entry)
    if source_rel == "AGENTS.md":
        return _deep_copy_json(ROOT_AGENTS_PAYLOAD)

    payload: dict[str, object] = {
        "entry_role": "repo_runtime_entry",
        "runtime_source_policy": _deep_copy_json(BASE_RUNTIME_SOURCE_POLICY),
        "default_meta_skill_order": list(DEFAULT_META_SKILL_ORDER),
        "peer_summary_policy": _peer_summary_policy(entry),
        "turn_start_actions": [
            "use the returned target contract JSON as the runtime rule source",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "do not use audit markdown as the primary execution guide",
            "stay within the concrete repo-local boundary defined by this payload",
        ],
        "turn_end_actions": [
            "follow repo-specific lint or Git duties only when they are explicitly listed in this payload",
        ],
    }

    if payload["peer_summary_policy"]["available"]:
        payload["runtime_constraints"].append(
            "same-level README.md remains a human summary; read it only when the current task needs that extra context"
        )

    if source_rel == "Codex_Skills_Mirror/AGENTS.md":
        payload["repo_name"] = "Codex_Skills_Mirror"
        payload["turn_start_actions"].append(
            "if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start"
        )
        payload["runtime_constraints"].append(
            "when this repo is written, keep same-turn Constitution lint and Git traceability in scope"
        )
        payload["turn_end_actions"] = [
            "run Constitution lint on the concrete Codex_Skills_Mirror target root",
            "if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn",
        ]
        return payload

    payload["repo_name"] = Path(entry["source_path"]).parent.name
    return payload


def build_target_contract(entry: dict[str, str], *, skill_root: Path) -> dict[str, object]:
    if is_agents_target_kind(entry["target_kind"]):
        return build_agents_payload(entry)

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
    payload = build_agents_payload(entry)
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
        "- If the returned payload includes `peer_summary_policy`, use it to decide whether the same-level README summary exists and whether it should be read.",
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
    if "peer_summary_policy" in payload:
        lines.extend(
            [
                "",
                "7. Peer Summary Policy",
                f"- {payload['peer_summary_policy']['guidance']}",
            ]
        )
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


def _load_agents_part_a(entry: dict[str, str]) -> str:
    source_path = Path(entry["source_path"])
    if _source_rel(entry) != "AGENTS.md":
        return render_external_agents(entry)
    if not source_path.exists():
        return ""
    return extract_part_a(source_path.read_text(encoding="utf-8"))


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
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if is_agents_target_kind(entry["target_kind"]):
            human_path = Path(entry["human_path"])
            human_path.parent.mkdir(parents=True, exist_ok=True)
            human_path.write_text(
                compose_managed_agents(_load_agents_part_a(entry), contract),
                encoding="utf-8",
            )
            for legacy in (
                legacy_runtime_json_path(skill_root, entry["managed_rel_path"], entry["target_kind"]),
                legacy_audit_md_path(skill_root, entry["managed_rel_path"], entry["target_kind"]),
            ):
                if legacy.exists():
                    legacy.unlink()
            written.extend([str(json_path), str(human_path)])
            continue
        md_path = audit_md_path(skill_root, entry)
        md_path.write_text(render_audit_markdown(contract), encoding="utf-8")
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
