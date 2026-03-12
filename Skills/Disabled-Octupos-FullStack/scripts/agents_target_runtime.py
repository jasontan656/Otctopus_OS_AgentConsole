from __future__ import annotations

import json
from pathlib import Path

HOOK_HEADER = "[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]"
PART_A_OPEN = "<part_A>"
PART_A_CLOSE = "</part_A>"
PART_B_OPEN = "<part_B>"
PART_B_CLOSE = "</part_B>"

ROOT_RELATIVE_PATH = "octopus_os_root"


def _resolve_product_root() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "octopus-os-agent-console"), None)
    if repo_root is None:
        raise RuntimeError("cannot resolve product root from Disabled-Octupos-FullStack script path")
    return repo_root.parent


DEFAULT_WORKSPACE_ROOT = (_resolve_product_root() / "Octopus_OS").resolve()


def managed_target_dir(skill_root: Path) -> Path:
    return skill_root / "assets" / "managed_targets" / "Octopus_OS"


def managed_human_path(skill_root: Path) -> Path:
    return managed_target_dir(skill_root) / "AGENTS_human.md"


def managed_machine_path(skill_root: Path) -> Path:
    return managed_target_dir(skill_root) / "AGENTS_machine.json"


def scan_report_path(skill_root: Path) -> Path:
    return skill_root / "assets" / "mother_doc_agents" / "scan_report.json"


def root_source_path(workspace_root: Path | None = None) -> Path:
    return (workspace_root or DEFAULT_WORKSPACE_ROOT) / "AGENTS.md"


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_tag_block(text: str, open_tag: str, close_tag: str) -> str | None:
    if open_tag not in text or close_tag not in text:
        return None
    return text.split(open_tag, 1)[1].split(close_tag, 1)[0].strip()


def extract_external_agents_part_a_body(text: str) -> str:
    tagged = _extract_tag_block(text, PART_A_OPEN, PART_A_CLOSE)
    if tagged is not None:
        return tagged
    return text.strip()


def render_external_agents(part_a_body: str) -> str:
    body = part_a_body.strip()
    return (
        f"{HOOK_HEADER}\n\n"
        "`HOOK_LOAD`: Apply this AGENTS contract.\n\n"
        f"{PART_A_OPEN}\n"
        f"{body}\n"
        f"{PART_A_CLOSE}\n"
    )


def extract_internal_part_a(human_text: str) -> str:
    if PART_B_OPEN in human_text:
        return human_text.split(PART_B_OPEN, 1)[0].rstrip() + "\n"
    return human_text.rstrip() + "\n"


def render_internal_agents_human(part_a_text: str, machine_payload: object) -> str:
    payload = json.dumps(machine_payload, indent=2, ensure_ascii=False)
    part_a = render_external_agents(extract_external_agents_part_a_body(part_a_text)).rstrip()
    return (
        f"{part_a}\n\n"
        f"{PART_B_OPEN}\n\n"
        f"```json\n{payload}\n```\n"
        f"{PART_B_CLOSE}\n"
    )


def _resolve_workspace_root(skill_root: Path) -> Path:
    report = scan_report_path(skill_root)
    if report.exists():
        payload = _load_json(report)
        raw_workspace_root = payload.get("workspace_root")
        if isinstance(raw_workspace_root, str):
            return Path(raw_workspace_root)
    sibling = skill_root.parent / "Octopus_OS"
    if (sibling / "AGENTS.md").exists():
        return sibling
    return DEFAULT_WORKSPACE_ROOT


def build_default_machine_payload() -> dict[str, object]:
    return {
        "entry_role": "octopus_os_root_runtime_entry",
        "runtime_source_policy": {
            "runtime_rule_source": "CLI_JSON",
            "audit_fields_are_not_primary_runtime_instructions": True,
            "path_metadata_is_not_action_guidance": True,
        },
        "turn_start_actions": [
            "use the returned target-contract JSON as the runtime rule source",
            "classify the turn as READ_EXEC or WRITE_EXEC",
            "treat Octopus_OS/AGENTS.md as the only external AGENTS runtime entry currently allowed in Octopus_OS",
        ],
        "runtime_constraints": [
            "treat CLI JSON as the primary runtime rule source",
            "use branch contract, stage directive, and target contract JSON as the runtime navigation chain",
            "all other AGENTS.md files under Octopus_OS are forbidden and must be cleaned by the AGENTS manager",
        ],
        "execution_modes": {
            "READ_EXEC": {
                "goal": "answer, inspect, classify, or route without changing files",
                "default_actions": [
                    "prefer direct CLI contract output over markdown rule files",
                ],
            },
            "WRITE_EXEC": {
                "goal": "edit the governed root AGENTS mapping or trigger the manager-owned write flows",
                "default_actions": [
                    "edit only the mirror-side managed target pair",
                    "use mother-doc-agents-push to write back the root AGENTS and clean forbidden external AGENTS files",
                ],
            },
        },
        "active_scope_policy": {
            "governed_external_target": str(root_source_path()),
            "managed_target_count": 1,
            "other_external_agents_forbidden": True,
        },
        "turn_end_actions": [
            "if the turn wrote Octopus_OS, run Constitution lint on the concrete target root",
            "if the turn changed the managed root AGENTS mapping, use mother-doc-agents-push before closing the turn",
        ],
    }


def load_machine_payload(skill_root: Path) -> dict[str, object]:
    path = managed_machine_path(skill_root)
    if not path.exists():
        return build_default_machine_payload()
    return _load_json(path)


def load_target_contract(skill_root: Path, relative_path: str, file_kind: str) -> dict[str, object]:
    if relative_path != ROOT_RELATIVE_PATH:
        raise ValueError(f"unsupported relative_path: {relative_path}")
    if file_kind != "agents":
        raise ValueError(f"unsupported file_kind: {file_kind}")
    workspace_root = _resolve_workspace_root(skill_root)
    payload = load_machine_payload(skill_root)
    return {
        "relative_path": ROOT_RELATIVE_PATH,
        "file_kind": "agents",
        "source_path": str(root_source_path(workspace_root)),
        "managed_human_path": str(managed_human_path(skill_root)),
        "managed_machine_path": str(managed_machine_path(skill_root)),
        "rule_source_policy": payload["runtime_source_policy"],
        "payload_navigation": {
            "branch_contract_cli": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/Cli_Toolbox.py mother-doc-agents-contract --json",
            "stage_directive_cli": "./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json",
        },
        "managed_asset_model": {
            "document_shape": {
                "external_shape": "part_a_only",
                "internal_human_shape": "part_a_plus_part_b",
                "internal_machine_shape": "part_b_only",
            },
            "governance_assets": {
                "managed_human_path": str(managed_human_path(skill_root)),
                "managed_machine_path": str(managed_machine_path(skill_root)),
                "scan_report_path": str(scan_report_path(skill_root)),
            },
        },
        "payload": payload,
    }
