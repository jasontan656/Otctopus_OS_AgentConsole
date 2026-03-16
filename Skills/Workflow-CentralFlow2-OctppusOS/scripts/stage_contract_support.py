from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from runtime_context_support import graph_core_command
from target_runtime_support import TargetRuntimeRecord, latest_archived_iteration, resolve_target_runtime
from workflow_stage_contract import STAGES


class StageDocContractPayload(TypedDict, total=False):
    stage: str
    resident_docs: list[str]
    stage_docs: list[str]
    drop_on_stage_switch: list[str]
    target_root: str
    docs_root: str
    mother_doc_root: str
    construction_plan_root: str
    iteration_context_root: str | None


class StageCommandContractPayload(TypedDict, total=False):
    stage: str
    entry_commands: list[str]
    gate_commands: list[str]
    optional_commands: list[str]
    required_iteration_actions: list[str]
    required_reuse_actions: list[str]
    required_runtime_actions: list[str]
    needs_real_env_threshold: list[str]


class StageGraphContractPayload(TypedDict):
    stage: str
    graph_role: str
    recommended_commands: list[str]


def stage_doc_contract_payload(
    stage: str,
    mother_doc_root: Path | None = None,
    target_runtime: TargetRuntimeRecord | None = None,
) -> StageDocContractPayload:
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
    if stage in {"mother_doc_audit", "mother_doc"} and mother_doc_root is not None:
        latest_archive = latest_archived_iteration(mother_doc_root)
        payload["iteration_context_root"] = str(latest_archive) if latest_archive else None
        if latest_archive is not None:
            payload["stage_docs"].append(str(latest_archive / "*"))
    return payload


def _runtime_cli_prefix(
    runtime: TargetRuntimeRecord,
    codebase_root: Path,
    graph_runtime_root: Path,
) -> str:
    target_root = Path(runtime["target_root"])
    docs_root = Path(runtime["docs_root"])
    parts = [
        "./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py",
        f"--target-root {target_root}",
        f"--development-docs-root {docs_root}",
        f"--docs-root {docs_root}",
        f"--codebase-root {codebase_root}",
        f"--graph-runtime-root {graph_runtime_root}",
    ]
    module_dir = runtime.get("module_dir")
    if isinstance(module_dir, str) and module_dir:
        parts.append(f"--module-dir {module_dir}")
    project_agents_path = runtime.get("project_agents_path")
    if project_agents_path is not None:
        parts.append(f"--project-agents {project_agents_path}")
    return " ".join(parts)


def stage_command_contract_payload(
    stage: str,
    mother_doc_root: Path,
    construction_plan_root: Path,
    codebase_root: Path,
    target_runtime: TargetRuntimeRecord | None = None,
) -> StageCommandContractPayload:
    runtime = target_runtime or resolve_target_runtime(
        docs_root=mother_doc_root.parent,
        codebase_root=codebase_root,
    )
    target_root = Path(runtime["target_root"])
    docs_root = Path(runtime["docs_root"])
    graph_runtime_root = Path(runtime["graph_runtime_root"])
    latest_archive = latest_archived_iteration(mother_doc_root)
    runtime_args = _runtime_cli_prefix(runtime, codebase_root, graph_runtime_root)
    target_runtime_cmd = f"{runtime_args} target-runtime-contract --json"
    checklist_cmd = f"{runtime_args} stage-checklist --stage {stage} --json"
    scaffold_cmd = f"{runtime_args} target-scaffold --json"

    commands = {
        "mother_doc_audit": {
            "entry_commands": [
                target_runtime_cmd,
                checklist_cmd,
                scaffold_cmd,
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-lint --path {mother_doc_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-audit --path {mother_doc_root} --json",
            ],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --allow-missing-index --json",
                graph_core_command(graph_runtime_root, "status", repo_cwd=codebase_root),
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-refresh-root-index --path {mother_doc_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-sync-client-copy --source {mother_doc_root} --mirror {runtime['client_mother_doc_root']} --json",
            ],
            "required_iteration_actions": [
                (
                    f"read the latest archived mother_doc iteration at {latest_archive} before deciding whether current growth debt is inherited or newly introduced"
                    if latest_archive is not None
                    else "if a numbered archived mother_doc iteration exists, read the latest archived sibling before classifying current growth debt"
                ),
                "run mother-doc-lint first so semantic audit never trusts a protocol-dirty tree",
                "run mother-doc-audit and classify blocking versus non-blocking growth debt before deeper mother_doc evidence reading",
                "prefer the registry-backed shadow split proposals from mother-doc-audit before inventing a custom split tree by hand",
                "when blocking debt exists, split or migrate the overloaded node first instead of pushing the polluted structure into mother_doc drafting",
                "before any audit-driven split uses a new vertical layer, branch family, or content family, register it in the skill and confirm it is reusable",
                "after audit-driven split writeback, rerun mother-doc-refresh-root-index, mother-doc-lint, and mother-doc-audit until the gate is clean",
            ],
        },
        "mother_doc": {
            "entry_commands": [
                target_runtime_cmd,
                checklist_cmd,
                scaffold_cmd,
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-lint --path {mother_doc_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-audit --path {mother_doc_root} --json",
            ],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --allow-missing-index --json",
                graph_core_command(graph_runtime_root, "status", repo_cwd=codebase_root),
                graph_core_command(graph_runtime_root, "analyze", str(codebase_root)),
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-refresh-root-index --path {mother_doc_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-mark-modified --path {mother_doc_root} --doc-ref <mother_doc_doc> --auto-from-git --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-sync-client-copy --source {mother_doc_root} --mirror {runtime['client_mother_doc_root']} --json",
            ],
            "required_iteration_actions": [
                "run Meta-Impact-Investigation in WRITE_INTENT mode before deciding this round's mother_doc write scope",
                (
                    f"read the latest archived mother_doc iteration at {latest_archive} before writing the new iteration"
                    if latest_archive is not None
                    else "if a numbered archived mother_doc iteration exists, read the latest archived sibling before writing the new iteration"
                ),
                "extract inherited target state, stable architecture decisions, unresolved blockers, and delivery deltas from the latest archived iteration",
                "inspect existing execution packs before deciding whether to init a new pack root or reuse the current task lineage",
                "if the repo already has substantive code, check Meta-code-graph-base runtime and initialize it when missing before finalizing tree growth decisions",
                "read graph context after archive review so the new mother_doc reflects current code reality rather than stale assumptions",
                "do not treat the current tree as a clean requirement source unless mother-doc-audit has already cleared blocking growth debt",
                "decide whether this round should extend vertically, branch horizontally, edit current nodes, migrate nodes, or delete nodes",
                "before creating a new vertical layer or horizontal branch family, register it in the skill and confirm it is reusable for sibling semantics",
                "reduce the current change into the smallest mother_doc write slice that can still close the intended semantic move",
                "after any mother_doc structural write, run mother-doc-refresh-root-index so 00_index.md is regenerated from the current folder tree",
                "after refreshing the root index, run mother-doc-sync-client-copy so the viewer-side Client_Applications/mother_doc mirror is brutally overwritten from the Development_Docs source tree",
                "after structural writeback, rerun mother-doc-audit so the next stage never inherits fresh growth debt",
            ],
        },
        "construction_plan": {
            "entry_commands": [
                target_runtime_cmd,
                checklist_cmd,
                scaffold_cmd,
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py construction-plan-lint --path {construction_plan_root} --json",
            ],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --allow-missing-index --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state modified --to-state planned --pack-ref <NN_slug> --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-mark-modified --path {mother_doc_root} --doc-ref <mother_doc_doc> --auto-from-git --json",
            ],
            "required_reuse_actions": [
                "classify any existing execution_atom_plan_validation_packs root before touching it: preview_skeleton must be replaced, accepted/retired plans must not be reused as fresh construction input",
                "do not create a second disconnected task-pack tree under a different docs container for the same target",
                "only an official_plan with plan_state=planned_unused or in_execution and current pack coverage may remain as the active plan root",
                "only move a mother_doc atom from modified to planned after an actual pack has absorbed it and the doc records that pack ref",
            ],
        },
        "implementation": {
            "entry_commands": [
                target_runtime_cmd,
                checklist_cmd,
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py construction-plan-lint --path {construction_plan_root} --require-execution-eligible --json",
            ],
            "optional_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state planned --to-state developed --pack-ref <NN_slug> --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-mark-modified --path {mother_doc_root} --doc-ref <design_doc> --auto-from-git --json",
            ],
            "required_reuse_actions": [
                "read only the active official pack in the current execution pack tree; preview skeletons and accepted/retired plans cannot enter implementation",
                "read only the source_mother_doc_refs declared by the active pack plus ref docs when truly needed",
            ],
        },
        "acceptance": {
            "entry_commands": [
                target_runtime_cmd,
                checklist_cmd,
            ],
            "gate_commands": [
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py acceptance-lint --codebase-root {codebase_root} --target-root {target_root} --development-docs-root {docs_root} --docs-root {docs_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --graph-runtime-root {graph_runtime_root} --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --path {mother_doc_root} --doc-ref <mother_doc_doc> --from-state developed --to-state ref --pack-ref <NN_slug> --json",
                f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py mother-doc-archive --target {mother_doc_root} --json",
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


def stage_graph_contract_payload(
    stage: str,
    codebase_root: Path,
    graph_runtime_root: Path | None = None,
) -> StageGraphContractPayload:
    graph_role = STAGES[stage]["graph_role"]
    graph_root = graph_runtime_root or resolve_target_runtime(codebase_root=codebase_root)[
        "graph_runtime_root"
    ]
    recommended_commands = {
        "mother_doc_audit": [
            f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_root} --allow-missing-index --json",
        ],
        "mother_doc": [
            f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_root} --allow-missing-index --json",
        ],
        "construction_plan": [
            f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-preflight --repo {codebase_root} --graph-runtime-root {graph_root} --allow-missing-index --json",
        ],
        "implementation": [],
        "acceptance": [
            f"./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py graph-postflight --repo {codebase_root} --graph-runtime-root {graph_root} --json",
        ],
    }
    return {
        "stage": stage,
        "graph_role": graph_role,
        "recommended_commands": recommended_commands[stage],
    }


stage_doc_contract_spec = stage_doc_contract_payload
stage_command_contract_spec = stage_command_contract_payload
stage_graph_contract_spec = stage_graph_contract_payload
