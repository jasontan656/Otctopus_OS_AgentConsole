from __future__ import annotations
from pathlib import Path
from workflow_stage_contract import STAGES
import re

# contract_name: octopus_backend_stage_contract_support
# contract_version: 1.0.0
# validation_mode: strict
# required_fields: stage_doc_contract_payload, stage_command_contract_payload, stage_graph_contract_payload
# optional_fields: []


ARCHIVE_DIR_PATTERN = re.compile(r"^(\d{2})_.+")


def _latest_archived_mother_doc(mother_doc_root: Path) -> Path | None:
    docs_root = mother_doc_root.parent
    candidates: list[tuple[int, Path]] = []
    for child in docs_root.iterdir():
        if not child.is_dir() or child.name == mother_doc_root.name:
            continue
        match = ARCHIVE_DIR_PATTERN.match(child.name)
        if match:
            candidates.append((int(match.group(1)), child))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def stage_doc_contract_payload(stage: str, mother_doc_root: Path | None = None) -> dict[str, object]:
    stage_data = STAGES[stage]
    payload = {
        "stage": stage,
        "resident_docs": stage_data["resident_docs"],
        "stage_docs": list(stage_data["stage_docs"]),
        "drop_on_stage_switch": stage_data["drop_on_stage_switch"],
    }
    if stage == "mother_doc" and mother_doc_root is not None:
        latest_archive = _latest_archived_mother_doc(mother_doc_root)
        payload["iteration_context_root"] = str(latest_archive) if latest_archive else None
        if latest_archive is not None:
            payload["stage_docs"].append(str(latest_archive / "*"))
    return payload


def stage_command_contract_payload(stage: str, mother_doc_root: Path, construction_plan_root: Path, codebase_root: Path) -> dict[str, object]:
    latest_archive = _latest_archived_mother_doc(mother_doc_root)
    commands = {
        "mother_doc": {
            "entry_commands": [
                f"python3 scripts/Cli_Toolbox.py stage-checklist --stage {stage} --json",
                f"python3 scripts/Cli_Toolbox.py mother-doc-init --target {mother_doc_root} --json",
            ],
            "gate_commands": [f"python3 scripts/Cli_Toolbox.py mother-doc-lint --path {mother_doc_root} --json"],
            "optional_commands": [f"python3 scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --allow-missing-index --json"],
            "required_iteration_actions": [
                (
                    f"read the latest archived mother_doc iteration at {latest_archive} before writing the new iteration"
                    if latest_archive is not None
                    else "if a numbered archived mother_doc iteration exists, read the latest archived sibling before writing the new iteration"
                ),
                "extract inherited target state, stable architecture decisions, unresolved blockers, and delivery deltas from the latest archived iteration",
                "read graph context after archive review so the new mother_doc reflects current code reality rather than stale assumptions",
            ],
        },
        "construction_plan": {
            "entry_commands": [
                f"python3 scripts/Cli_Toolbox.py stage-checklist --stage {stage} --json",
                f"python3 scripts/Cli_Toolbox.py construction-plan-init --target {construction_plan_root} --json",
            ],
            "gate_commands": [f"python3 scripts/Cli_Toolbox.py construction-plan-lint --path {construction_plan_root} --json"],
            "optional_commands": [f"python3 scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --allow-missing-index --json"],
        },
        "implementation": {
            "entry_commands": [f"python3 scripts/Cli_Toolbox.py stage-checklist --stage {stage} --json"],
            "gate_commands": [],
            "optional_commands": [],
        },
        "acceptance": {
            "entry_commands": [f"python3 scripts/Cli_Toolbox.py stage-checklist --stage {stage} --json"],
            "gate_commands": [
                "python3 scripts/Cli_Toolbox.py acceptance-lint --json",
                f"python3 scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --json",
                f"python3 scripts/Cli_Toolbox.py mother-doc-archive --target {mother_doc_root} --json",
            ],
            "optional_commands": [],
            "required_runtime_actions": [
                "read 07_env_and_deploy.md, 10_observability_and_evidence.md, 11_risks_and_blockers.md, and codebase AGENTS before deciding needs_real_env",
                "resolve secrets from local ignored env files or other non-git secret sources declared by the project; do not expect tokens inside mother doc or pushable runtime docs",
                "apply env/config/unit/webhook/ngrok settings to the local WSL environment until the runtime is actually runnable",
                "start resident services and verify healthz plus concrete db/redis/mq/webhook connectivity",
                "simulate at least one human interaction through the real local stack and capture service logs, db rows, queue events, redis keys, and outbound delivery evidence",
            ],
            "needs_real_env_threshold": [
                "only after local config, service bring-up, health checks, and simulated human usage have been attempted",
                "only for truly external blockers such as missing third-party credentials, account control, or remote resources outside local control",
            ],
        },
    }
    return {"stage": stage, **commands[stage]}


def stage_graph_contract_payload(stage: str, codebase_root: Path) -> dict[str, object]:
    graph_role = STAGES[stage]["graph_role"]
    recommended_commands = {
        "mother_doc": [f"python3 scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --allow-missing-index --json"],
        "construction_plan": [f"python3 scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --allow-missing-index --json"],
        "implementation": [],
        "acceptance": [f"python3 scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --json"],
    }
    return {"stage": stage, "graph_role": graph_role, "recommended_commands": recommended_commands[stage]}
