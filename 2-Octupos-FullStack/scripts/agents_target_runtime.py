from __future__ import annotations

import json
from pathlib import Path

ROOT_BRANCH = "octopus_os_root"
CONTAINER_BRANCH = "container_roots"
DOCS_BRANCH = "mother_doc_docs"
AGENT_AUDIT_FILENAME = "AGENT_AUDIT.md"
README_AUDIT_FILENAME = "README_AUDIT.md"
MIRROR_CLI = "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack/scripts/Cli_Toolbox.py"


def runtime_rule_root(skill_root: Path) -> Path:
    return skill_root / "assets" / "mother_doc_agents" / "runtime_rules"


def runtime_json_path(skill_root: Path, relative_path: str, file_kind: str) -> Path:
    return runtime_rule_root(skill_root) / Path(relative_path) / ("AGENTS.runtime.json" if file_kind == "agents" else "README.runtime.json")


def audit_md_path(skill_root: Path, relative_path: str, file_kind: str) -> Path:
    return runtime_rule_root(skill_root) / Path(relative_path) / (AGENT_AUDIT_FILENAME if file_kind == "agents" else README_AUDIT_FILENAME)


def template_asset_path(skill_root: Path, relative_path: str, file_kind: str) -> Path:
    filename = "AGENTS.md" if file_kind == "agents" else "README.md"
    return skill_root / "assets" / "mother_doc_agents" / "templates" / Path(relative_path) / filename


def collected_snapshot_path(skill_root: Path, relative_path: str, file_kind: str) -> Path:
    filename = "AGENTS.md" if file_kind == "agents" else "README.md"
    return skill_root / "assets" / "mother_doc_agents" / "collected_tree" / Path(relative_path) / filename


def _peer_doc(entry: dict[str, str], file_kind: str) -> dict[str, str]:
    if file_kind == "agents":
        return {
            "path": entry["readme_source_path"],
            "relation": "same_level_summary",
            "read_policy": "optional_then_required_on_write_if_exists",
        }
    return {
        "path": entry["agents_source_path"],
        "relation": "same_level_runtime_entry",
        "read_policy": "required_first_if_exists",
    }


def _turn_contract(relative_path: str, file_kind: str) -> dict[str, object]:
    if relative_path == ROOT_BRANCH and file_kind == "agents":
        return {
            "status": "enforced",
            "turn_start": [
                "if the turn will write Octopus_OS, plan same-turn Constitution lint from the start",
                "use the returned target contract JSON as the runtime rule source",
            ],
            "turn_end": [
                "if the turn wrote Octopus_OS, run Constitution lint on the concrete target root",
            ],
        }
    return {
        "status": "n_a",
        "turn_start": ["N/A"],
        "turn_end": ["N/A"],
    }


def _document_shape(entry: dict[str, str], file_kind: str) -> dict[str, object]:
    if file_kind == "agents":
        return {
            "external_shape": "thin_runtime_entry_only",
            "skill_side_primary_runtime_asset": "runtime_json",
            "skill_side_audit_asset": "audit_markdown_only",
            "push_behavior": "regenerate_external_entry_from_skill_runtime",
            "collect_behavior": "capture_current_external_entry_as_snapshot",
        }
    if entry["readme_management_mode"] == "template_managed":
        return {
            "external_shape": "human_summary_only",
            "skill_side_primary_runtime_asset": "template_and_snapshot_pair",
            "skill_side_audit_asset": "collected_snapshot_plus_registry",
            "push_behavior": "overwrite_external_readme_from_skill_template",
            "collect_behavior": "capture_current_external_readme_as_snapshot",
        }
    return {
        "external_shape": "human_summary_only",
        "skill_side_primary_runtime_asset": "collected_snapshot_first",
        "skill_side_audit_asset": "template_mirror_and_registry",
        "push_behavior": "preserve_external_readme_current_state_unless_navigation_initializes_missing_file",
        "collect_behavior": "external_readme_is_the_current_state_truth",
    }


def _execution_modes(file_kind: str) -> dict[str, object]:
    shared_write_actions = [
        "state the concrete write scope before editing",
        "stay within the returned update_boundary and routing rules",
        "re-read the peer document when the peer_doc policy upgrades from optional to required on write",
    ]
    if file_kind == "agents":
        shared_write_actions.append("treat this target contract JSON as the runtime source of truth instead of the local markdown entry body")
    else:
        shared_write_actions.append("treat this README as human summary only and pair it with the same-scope AGENTS target contract on writes")
    return {
        "READ_EXEC": {
            "goal": "classify the current scope, decide next hop, and inspect without rewriting files",
            "default_actions": [
                "prefer the returned JSON payload over audit markdown",
                "read the peer document only when peer_doc says required or when the task explicitly needs human summary context",
            ],
        },
        "WRITE_EXEC": {
            "goal": "update the concrete AGENTS or README scope without drifting outside this target boundary",
            "default_actions": shared_write_actions,
        },
    }


def _runtime_constraints(entry: dict[str, str], file_kind: str) -> list[str]:
    constraints = [
        "treat CLI JSON as the primary runtime rule source",
        "do not use audit markdown as the primary execution guide",
        "path metadata is not action guidance by itself; use routing, update_boundary, and execution_modes together",
        "do not open extra branch markdown files just to discover the next command when this payload already provides it",
    ]
    if file_kind == "agents":
        constraints.append("AGENTS external files stay thin; detailed routing and update boundaries live in the returned JSON payload")
    elif entry["readme_management_mode"] == "collect_preserve":
        constraints.append("Mother_Doc docs README current state is preserved by collect; do not overwrite it from stale template assumptions")
    else:
        constraints.append("Root and container README files are template-managed human summaries and must stay aligned with the generated templates")
    return constraints


def build_target_contract(entry: dict[str, str], *, skill_root: Path, file_kind: str) -> dict[str, object]:
    relative_path = entry["relative_path"]
    branch = entry["scope_branch"]
    target_cli = (
        f'python3 {MIRROR_CLI} mother-doc-agents-target-contract '
        f'--relative-path "{relative_path}" --file-kind {file_kind} --json'
    )
    contract = {
        "schema_version": 1,
        "owner_skill": "2-Octupos-FullStack",
        "managed_branch": "mother_doc_agents_readme",
        "rule_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
            "human_audit_source": "audit_markdown_only",
            "model_must_not_read_markdown_for_runtime_guidance": True,
        },
        "target": {
            "scope_branch": branch,
            "relative_path": relative_path,
            "scope_path": entry["scope_path"],
            "file_kind": file_kind,
            "source_path": entry["agents_source_path"] if file_kind == "agents" else entry["readme_source_path"],
            "peer_path": entry["readme_source_path"] if file_kind == "agents" else entry["agents_source_path"],
            "readme_management_mode": entry["readme_management_mode"],
        },
        "peer_doc": _peer_doc(entry, file_kind),
        "turn_start_actions": [
            "load and follow this target contract JSON before using any path-local AGENTS or README prose as guidance",
            "use peer_doc.read_policy to decide whether the same-level peer file must also be read",
            "classify the task as READ_EXEC or WRITE_EXEC before acting",
        ],
        "runtime_constraints": _runtime_constraints(entry, file_kind),
        "forbidden_primary_runtime_pattern": [
            "Do not treat audit markdown paths as the main runtime instructions.",
            "Do not require the model to open a chain of markdown files just to learn the next target or command.",
            "Do not emit only path metadata when the real need is direct action guidance.",
        ],
        "execution_modes": _execution_modes(file_kind),
        "managed_asset_model": {
            "scope_branch": branch,
            "file_kind": file_kind,
            "readme_management_mode": entry["readme_management_mode"],
            "document_shape": _document_shape(entry, file_kind),
            "governance_assets": {
                "runtime_json_path": str(runtime_json_path(skill_root, relative_path, file_kind)),
                "audit_md_path": str(audit_md_path(skill_root, relative_path, file_kind)),
                "template_path": str(template_asset_path(skill_root, relative_path, file_kind)),
                "collected_snapshot_path": str(collected_snapshot_path(skill_root, relative_path, file_kind)),
            },
        },
        "runtime_entry": {
            "cli": target_cli,
            "runtime_json_path": str(runtime_json_path(skill_root, relative_path, file_kind)),
            "audit_md_path": str(audit_md_path(skill_root, relative_path, file_kind)),
        },
        "payload_navigation": {
            "branch_contract_cli": f"python3 {MIRROR_CLI} mother-doc-agents-contract --json",
            "stage_directive_cli": f"python3 {MIRROR_CLI} mother-doc-agents-directive --stage <scan|collect|push> --json",
            "branch_registry_cli": f"python3 {MIRROR_CLI} mother-doc-agents-registry --json",
            "current_target_cli": target_cli,
        },
        "human_audit_sources": [
            str(audit_md_path(skill_root, relative_path, file_kind)),
            str(skill_root / "references" / "mother_doc" / "agents_branch" / "runtime" / "AGENTS_BRANCH_CONTRACT.md"),
        ],
        "turn_contract": _turn_contract(relative_path, file_kind),
        "routing": {
            "document_role": "runtime_entry" if file_kind == "agents" else "human_summary",
            "default_next_hop": "",
            "rules": [],
        },
        "update_boundary": [],
    }
    if branch == ROOT_BRANCH:
        contract["routing"] = {
            "document_role": "runtime_entry" if file_kind == "agents" else "human_summary",
            "default_next_hop": "select stage first, then choose Octopus_OS container path or Mother_Doc path",
            "rules": [
                "use 2-Octupos-FullStack CLI outputs as the runtime rule source",
                "README remains a human summary file",
            ],
        }
        contract["update_boundary"] = [
            "Octopus_OS root AGENTS is a thin runtime entry",
            "detailed runtime rules stay in skill-managed JSON and CLI output",
        ]
    elif branch == CONTAINER_BRANCH:
        contract["routing"] = {
            "document_role": "runtime_entry" if file_kind == "agents" else "human_summary",
            "default_next_hop": "decide between current container code path and the matching Mother_Doc/docs path",
            "rules": [
                "for doc design or scope browsing, prefer the matching Mother_Doc/docs path",
                "for code/runtime work, stay in the container path and pair it with Mother_Doc/docs/<Container>/common",
                "for User_UI/Admin_UI browser tasks, load Meta-browser-operation",
            ],
        }
        contract["update_boundary"] = [
            "container-root AGENTS only governs root entry and paired document navigation",
            "README remains a human summary and must be checked on writes",
        ]
    elif branch == DOCS_BRANCH:
        contract["routing"] = {
            "document_role": "runtime_entry" if file_kind == "agents" else "human_summary",
            "default_next_hop": "use the current scope to choose the next child scope or leaf",
            "rules": [
                "stay inside the affected Mother_Doc/docs subtree",
                "AGENTS only points to the next hop; runtime rules live in the returned JSON",
            ],
        }
        contract["update_boundary"] = [
            "mother_doc_docs AGENTS is a recursive runtime entry",
            "README remains current-scope human summary; peer scope doc remains explicit scope description",
        ]
    return contract


def render_external_agents(relative_path: str) -> str:
    command = (
        f'python3 {MIRROR_CLI} mother-doc-agents-target-contract '
        f'--relative-path "{relative_path}" --file-kind agents --json'
    )
    turn_contract = _turn_contract(relative_path, "agents")
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
        "3. Peer Read Gate",
        "- See the returned `peer_doc` object to decide whether the same-level peer file must be read.",
        "",
        "[EXECUTION - MANDATORY]",
        "",
        "4. Runtime Rule Source",
        "- The returned JSON is the runtime rule source for this path.",
        "- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.",
        "",
        "5. Routing",
        "- Use the returned `routing` and `update_boundary` fields instead of reading extra markdown for runtime rules.",
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
    runtime_entry = contract["runtime_entry"]
    peer_doc = contract["peer_doc"]
    turn_contract = contract["turn_contract"]
    lines = [
        "# Target Rule Audit",
        "",
        "> Human audit copy generated from the skill-managed target runtime JSON.",
        "> Runtime models must call the listed CLI instead of reading this markdown.",
        "",
        "## Target",
        f"- relative_path: `{target['relative_path']}`",
        f"- scope_branch: `{target['scope_branch']}`",
        f"- file_kind: `{target['file_kind']}`",
        f"- source_path: `{target['source_path']}`",
        "",
        "## Runtime Entry",
        f"- cli: `{runtime_entry['cli']}`",
        f"- runtime_json_path: `{runtime_entry['runtime_json_path']}`",
        "",
        "## Managed Asset Model",
        f"- external_shape: `{contract['managed_asset_model']['document_shape']['external_shape']}`",
        f"- push_behavior: `{contract['managed_asset_model']['document_shape']['push_behavior']}`",
        f"- collect_behavior: `{contract['managed_asset_model']['document_shape']['collect_behavior']}`",
        f"- template_path: `{contract['managed_asset_model']['governance_assets']['template_path']}`",
        f"- collected_snapshot_path: `{contract['managed_asset_model']['governance_assets']['collected_snapshot_path']}`",
        "",
        "## Peer Doc",
        f"- path: `{peer_doc['path']}`",
        f"- read_policy: `{peer_doc['read_policy']}`",
        "",
        "## Runtime Constraints",
    ]
    lines.extend([f"- {item}" for item in contract["runtime_constraints"]])
    lines.extend(
        [
        "",
        "## Turn Contract",
        f"- status: `{turn_contract['status']}`",
        "- turn_start:",
        ]
    )
    lines.extend([f"  - {item}" for item in turn_contract["turn_start"]])
    lines.append("- turn_end:")
    lines.extend([f"  - {item}" for item in turn_contract["turn_end"]])
    lines.append("")
    return "\n".join(lines)


def write_target_contract_assets(skill_root: Path, entries: list[dict[str, str]]) -> list[str]:
    written: list[str] = []
    for entry in entries:
        for file_kind in ("agents", "readme"):
            contract = build_target_contract(entry, skill_root=skill_root, file_kind=file_kind)
            json_path = runtime_json_path(skill_root, entry["relative_path"], file_kind)
            md_path = audit_md_path(skill_root, entry["relative_path"], file_kind)
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            md_path.write_text(render_audit_markdown(contract), encoding="utf-8")
            written.extend([str(json_path), str(md_path)])
    return written


def load_target_contract(skill_root: Path, relative_path: str, file_kind: str) -> dict[str, object]:
    registry_path = skill_root / "assets" / "mother_doc_agents" / "registry.json"
    if not registry_path.exists():
        raise FileNotFoundError(f"registry missing: {registry_path}")
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in payload.get("entries", []):
        if entry["relative_path"] == relative_path:
            return build_target_contract(entry, skill_root=skill_root, file_kind=file_kind)
    raise ValueError(f"relative_path not found in registry: {relative_path}")
