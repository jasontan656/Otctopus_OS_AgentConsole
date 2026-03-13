from __future__ import annotations
from pathlib import Path
from workflow_stage_contract import STAGES
import re
from target_runtime_support import latest_archived_iteration, resolve_target_runtime

# contract_name: octopus_devflow_stage_contract_support
# contract_version: 1.0.0
# validation_mode: strict
# required_fields: stage_doc_contract_payload, stage_command_contract_payload, stage_graph_contract_payload
# optional_fields: []


ARCHIVE_DIR_PATTERN = re.compile(r"^(\d{2})_.+")


def stage_doc_contract_payload(
    stage: str,
    mother_doc_root: Path | None = None,
    target_runtime: dict[str, object] | None = None,
) -> dict[str, object]:
    stage_data = STAGES[stage]
    payload = {
        "stage": stage,
        "resident_docs": stage_data["resident_docs"],
        "stage_docs": list(stage_data["stage_docs"]),
        "drop_on_stage_switch": stage_data["drop_on_stage_switch"],
    }
    if target_runtime is not None:
        payload["target_root"] = str(target_runtime["target_root"])
        payload["docs_root"] = str(target_runtime["docs_root"])
        payload["mother_doc_root"] = str(target_runtime["mother_doc_root"])
        payload["construction_plan_root"] = str(target_runtime["construction_plan_root"])
    if stage == "mother_doc" and mother_doc_root is not None:
        latest_archive = latest_archived_iteration(mother_doc_root)
        payload["iteration_context_root"] = str(latest_archive) if latest_archive else None
        if latest_archive is not None:
            payload["stage_docs"].append(str(latest_archive / "*"))
    return payload


def stage_command_contract_payload(
    stage: str,
    mother_doc_root: Path,
    construction_plan_root: Path,
    codebase_root: Path,
    target_runtime: dict[str, object] | None = None,
) -> dict[str, object]:
    runtime = target_runtime or resolve_target_runtime(
        docs_root=mother_doc_root.parent,
        codebase_root=codebase_root,
    )
    target_root = Path(runtime["target_root"])
    development_docs_root = Path(runtime["development_docs_root"])
    docs_root = Path(runtime["docs_root"])
    graph_runtime_root = Path(runtime["graph_runtime_root"])
    project_agents_path = runtime["project_agents_path"]
    latest_archive = latest_archived_iteration(mother_doc_root)
    target_runtime_cmd_parts = [
        "./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-runtime-contract",
        f"--target-root {target_root}",
        f"--development-docs-root {development_docs_root}",
        f"--docs-root {docs_root}",
        f"--module-dir {runtime['module_dir']}",
        f"--codebase-root {codebase_root}",
        f"--graph-runtime-root {graph_runtime_root}",
    ]
    if project_agents_path is not None:
        target_runtime_cmd_parts.append(f"--project-agents {project_agents_path}")
    target_runtime_cmd_parts.append("--json")
    target_runtime_cmd = " ".join(target_runtime_cmd_parts)
    commands = {
        "mother_doc": {
            "entry_commands": [
                target_runtime_cmd,
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-checklist --stage {stage} --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-scaffold --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
            ],
            "gate_commands": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py mother-doc-lint --path {mother_doc_root} --json"],
            "optional_commands": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --allow-missing-index --json"],
            "required_iteration_actions": [
                (
                    f"read the latest archived mother_doc iteration at {latest_archive} before writing the new iteration"
                    if latest_archive is not None
                    else "if a numbered archived mother_doc iteration exists, read the latest archived sibling before writing the new iteration"
                ),
                "extract inherited target state, stable architecture decisions, unresolved blockers, and delivery deltas from the latest archived iteration",
                "inspect existing execution packs before deciding whether to init a new pack root or reuse the current task lineage",
                "read graph context after archive review so the new mother_doc reflects current code reality rather than stale assumptions",
            ],
        },
        "construction_plan": {
            "entry_commands": [
                target_runtime_cmd,
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-checklist --stage {stage} --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-scaffold --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
            ],
            "gate_commands": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py construction-plan-lint --path {construction_plan_root} --json"],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --allow-missing-index --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state modified --to-state planned --pack-ref <NN_slug> --json",
            ],
            "required_reuse_actions": [
                "reuse the existing execution_atom_plan_validation_packs root when it is already present",
                "do not create a second disconnected task-pack tree under a different docs container for the same target",
                "only move a mother_doc atom from modified to planned after an actual pack has absorbed it and the doc records that pack ref",
            ],
        },
        "implementation": {
            "entry_commands": [
                target_runtime_cmd,
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-checklist --stage {stage} --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
            ],
            "gate_commands": [],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state planned --to-state developed --pack-ref <NN_slug> --json",
            ],
            "required_reuse_actions": [
                "read only the active pack in the current execution pack tree; do not fork implementation onto a new disconnected pack set",
                "read only the source_mother_doc_refs declared by the active pack plus ref docs when truly needed",
            ],
        },
        "acceptance": {
            "entry_commands": [
                target_runtime_cmd,
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py stage-checklist --stage {stage} --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --module-dir {runtime['module_dir']} --codebase-root {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py acceptance-lint --codebase-root {codebase_root} --target-root {target_root} --development-docs-root {development_docs_root} --docs-root {docs_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state developed --to-state ref --pack-ref <NN_slug> --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py mother-doc-archive --target {mother_doc_root} --json",
            ],
            "optional_commands": [],
            "required_runtime_actions": [
                "read 07_env_and_deploy.md, 10_observability_and_evidence.md, 11_risks_and_blockers.md, and project AGENTS before deciding needs_real_env",
                "resolve secrets or credentials from local ignored env files or other non-git secret sources declared by the project; do not expect secrets inside mother doc or pushable runtime docs",
                "apply project-declared env/config/startup settings to the local environment until the runtime or workspace is actually runnable",
                "start the project-declared runtime surfaces and verify health plus dependency connectivity",
                "simulate at least one real operator or human path through the local stack and capture logs, files, traces, UI witness, or delivery evidence",
            ],
            "needs_real_env_threshold": [
                "only after local config, runtime bring-up, health checks, and simulated usage have been attempted",
                "only for truly external blockers such as missing third-party credentials, account control, or remote resources outside local control",
            ],
        },
    }
    return {"stage": stage, **commands[stage]}


def stage_graph_contract_payload(stage: str, codebase_root: Path, graph_runtime_root: Path | None = None) -> dict[str, object]:
    graph_role = STAGES[stage]["graph_role"]
    graph_root = graph_runtime_root or resolve_target_runtime(codebase_root=codebase_root)["graph_runtime_root"]
    recommended_commands = {
        "mother_doc": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_root} --allow-missing-index --json"],
        "construction_plan": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_root} --allow-missing-index --json"],
        "implementation": [],
        "acceptance": [f"./.venv_backend_skills/bin/python Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --graph-runtime-root {graph_root} --json"],
    }
    return {"stage": stage, "graph_role": graph_role, "recommended_commands": recommended_commands[stage]}
