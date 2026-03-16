from __future__ import annotations

import os
import shlex
from pathlib import Path


STAGE_TO_SKILL = {
    "mother_doc": "Workflow-MotherDoc-OctopusOS",
    "construction_plan": "Workflow-ConstructionPlan-OctopusOS",
    "implementation": "Workflow-Implementation-OctopusOS",
    "acceptance": "Workflow-Acceptance-OctopusOS",
}

SKILL_TO_STAGE = {value: key for key, value in STAGE_TO_SKILL.items()}

COMMON_COMMANDS = {
    "contract",
    "runtime-contract",
    "read-contract-context",
    "read-path-context",
    "workflow-contract",
    "target-runtime-contract",
    "stage-checklist",
    "stage-doc-contract",
    "stage-command-contract",
    "stage-graph-contract",
    "template-index",
}

STAGE_COMMANDS = {
    "mother_doc": COMMON_COMMANDS
    | {
        "graph-preflight",
        "target-scaffold",
        "mother-doc-audit",
        "mother-doc-init",
        "mother-doc-archive",
        "mother-doc-lint",
        "mother-doc-refresh-root-index",
        "mother-doc-state-sync",
        "mother-doc-mark-modified",
        "mother-doc-sync-client-copy",
    },
    "construction_plan": COMMON_COMMANDS
    | {
        "graph-preflight",
        "construction-plan-init",
        "construction-plan-lint",
        "mother-doc-state-sync",
        "mother-doc-mark-modified",
    },
    "implementation": COMMON_COMMANDS
    | {
        "construction-plan-lint",
        "mother-doc-state-sync",
        "mother-doc-mark-modified",
    },
    "acceptance": COMMON_COMMANDS
    | {
        "graph-postflight",
        "acceptance-lint",
        "mother-doc-state-sync",
        "mother-doc-archive",
    },
}


def active_skill_root() -> Path:
    configured = os.environ.get("OCTOPUS_WORKFLOW_ACTIVE_SKILL_ROOT", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    raise RuntimeError("OCTOPUS_WORKFLOW_ACTIVE_SKILL_ROOT is required for Octopus workflow runtime")


def active_skill_name() -> str:
    configured = os.environ.get("OCTOPUS_WORKFLOW_ACTIVE_SKILL_NAME", "").strip()
    if configured:
        return configured
    return active_skill_root().name


def active_stage() -> str:
    configured = os.environ.get("OCTOPUS_WORKFLOW_ACTIVE_STAGE", "").strip()
    if configured:
        return configured
    skill_name = active_skill_name()
    if skill_name in SKILL_TO_STAGE:
        return SKILL_TO_STAGE[skill_name]
    raise RuntimeError(f"cannot infer active stage for skill {skill_name}")


def allowed_commands() -> set[str]:
    return set(STAGE_COMMANDS[active_stage()])


def stage_choices() -> list[str]:
    return [active_stage()]


def top_level_resident_docs() -> list[str]:
    return [
        "path/stage_flow/10_CONTRACT.md",
        "path/stage_flow/15_TOOLS.md",
    ]


def stage_flow_glob() -> str:
    return f"Skills/{active_skill_name()}/path/stage_flow/*"


def cli_relative_path() -> str:
    return f"Skills/{active_skill_name()}/scripts/Cli_Toolbox.py"


def cli_prefix() -> str:
    return f"./.venv_backend_skills/bin/python {cli_relative_path()}"


def cli_command(*parts: object) -> str:
    quoted = " ".join(shlex.quote(str(part)) for part in parts)
    if quoted:
        return f"{cli_prefix()} {quoted}"
    return cli_prefix()


def repo_root_from_skill() -> Path:
    return active_skill_root().parents[1]


def mother_doc_agents_root() -> Path:
    return active_skill_root() / "assets" / "agents"


def mother_doc_audit_registry_path() -> Path:
    return active_skill_root() / "assets" / "mother_doc_audit" / "split_decision_registry.json"


def available_template_paths() -> dict[str, Path]:
    stage = active_stage()
    skill_root = active_skill_root()
    if stage == "mother_doc":
        return {
            "mother_doc_root": skill_root / "assets" / "mother_doc",
            "mother_doc_index": skill_root / "assets" / "mother_doc" / "00_index.md",
            "requirement_atom": skill_root / "assets" / "REQUIREMENT_ATOM_TEMPLATE.md",
            "agents_external_entry": skill_root / "assets" / "agents" / "EXTERNAL_AGENTS.md",
            "agents_machine_payload": skill_root / "assets" / "agents" / "AGENTS_MACHINE_TEMPLATE.json",
        }
    if stage == "construction_plan":
        return {
            "construction_plan_root": skill_root / "assets" / "execution_atom_plan_validation_packs",
            "construction_plan_index": skill_root / "assets" / "execution_atom_plan_validation_packs" / "00_index.md",
            "execution_atom_pack_template_root": skill_root / "assets" / "execution_atom_plan_validation_packs" / "PACK_TEMPLATE",
        }
    if stage == "acceptance":
        return {
            "acceptance_report": skill_root / "assets" / "acceptance" / "ACCEPTANCE_REPORT_TEMPLATE.md",
            "acceptance_matrix": skill_root / "assets" / "acceptance" / "ACCEPTANCE_MATRIX_TEMPLATE.md",
        }
    return {}
