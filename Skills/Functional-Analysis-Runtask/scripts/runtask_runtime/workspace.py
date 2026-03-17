from __future__ import annotations

from pathlib import Path

import yaml

from .catalog import STAGE_ARTIFACTS, STAGE_ORDER, STAGE_REQUIRED_SECTIONS, STAGE_TITLES, STAGE_UPSTREAM_REPORTS, WORKSPACE_LAYOUT
from .task_runtime import normalize_numbered_workspace_root, task_gate_check_payload, workspace_root_boundary_error
from .types import BoundaryErrorPayload, TaskGateCheckPayload, WorkspaceScaffoldPayload


def scaffold_workspace(workspace_root: Path, force: bool = False) -> WorkspaceScaffoldPayload | BoundaryErrorPayload | TaskGateCheckPayload:
    requested_workspace_root = workspace_root.resolve()
    boundary_error = workspace_root_boundary_error(requested_workspace_root)
    if boundary_error is not None:
        return boundary_error
    normalized_workspace_root = normalize_numbered_workspace_root(requested_workspace_root)
    if not normalized_workspace_root.exists():
        gate_payload = task_gate_check_payload()
        if gate_payload["status"] != "ok":
            return {
                "status": "fail",
                "workspace_root": str(normalized_workspace_root),
                "requested_workspace_root": str(requested_workspace_root),
                "created_files": [],
                "skipped_files": [],
                "workspace_layout": WORKSPACE_LAYOUT,
                "stage_artifacts": STAGE_ARTIFACTS,
                "reason": "unfinished_task_exists",
                "task_runtime_root": gate_payload["task_runtime_root"],
                "open_tasks": [{"task_root": item["task_root"], "reason": item.get("reason", ""), "resume_hint": item["resume_hint"]} for item in gate_payload["open_tasks"]],
                "message": "存在未闭合历史任务，禁止创建新 workspace；请先 resume 或 closed 对应 task_runtime.yaml。",
            }
    manifest = {
        "analysis_id": "fill_me",
        "intent_summary": "fill_me",
        "execution_mode": "continuous",
        "single_stage_focus": None,
        "current_stage": "research",
        "source_assets": [],
        "target_scope": {"external_target": "", "local_target": ""},
        "stage_status": {stage: ("in_progress" if stage == "research" else "pending") for stage in STAGE_ORDER},
        "stage_outputs": dict(STAGE_ARTIFACTS),
        "writeback_status": {
            "current_sync_report": STAGE_ARTIFACTS["validation"],
            "final_delivery_brief": STAGE_ARTIFACTS["final_delivery"],
            "last_synced_at": "",
            "notes": "",
        },
    }
    objects = {
        WORKSPACE_LAYOUT["manifest"]: manifest,
        WORKSPACE_LAYOUT["evidence_registry"]: {"evidence_items": []},
        WORKSPACE_LAYOUT["architect_assessment"]: {
            "consumed_stage_reports": list(STAGE_UPSTREAM_REPORTS["architect"]),
            "question_framework": [],
            "judgement_chain": [],
            "should_change": [],
            "should_not_change": [],
            "open_questions": [],
            "architecture_judgement": "",
            "evidence_refs": [],
        },
        WORKSPACE_LAYOUT["preview_projection"]: {
            "consumed_stage_reports": list(STAGE_UPSTREAM_REPORTS["preview"]),
            "question_framework": [],
            "reasoning_chain": [],
            "future_shape": [],
            "behavior_delta": [],
            "failure_modes": [],
            "rollback_triggers": [],
            "evidence_refs": [],
        },
        WORKSPACE_LAYOUT["design_decisions"]: {
            "consumed_stage_reports": list(STAGE_UPSTREAM_REPORTS["design"]),
            "question_framework": [],
            "decision_mode": "rewrite",
            "seamless_state": "",
            "decision_chain": [],
            "decision_items": [],
            "evidence_refs": [],
        },
        WORKSPACE_LAYOUT["impact_map"]: {
            "task_mode": "WRITE_INTENT",
            "consumed_stage_reports": list(STAGE_UPSTREAM_REPORTS["impact"]),
            "question_framework": [],
            "judgement_chain": [],
            "direct_scope": [],
            "indirect_scope": [],
            "latent_related": [],
            "validation_or_evidence": [],
            "must_update": [],
            "must_check_before_edit": [],
            "regression_surface": [],
            "evidence_refs": [],
            "confidence": "",
            "evidence_gaps": [],
        },
        WORKSPACE_LAYOUT["milestone_packages"]: {
            "planning_basis": {
                "consumed_stage_reports": list(STAGE_UPSTREAM_REPORTS["plan"]),
                "question_framework": [],
                "package_derivation_chain": [],
            },
            "milestone_packages": [],
        },
        WORKSPACE_LAYOUT["implementation_ledger"]: {"entries": []},
    }
    created: list[str] = []
    skipped: list[str] = []
    for relative, payload in objects.items():
        target = normalized_workspace_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(relative)
            continue
        target.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(relative)
    for stage, relative in STAGE_ARTIFACTS.items():
        target = normalized_workspace_root / relative
        if target.suffix != ".md":
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(relative)
            continue
        target.write_text(stage_artifact_template(stage), encoding="utf-8")
        created.append(relative)
    return {
        "status": "ok",
        "workspace_root": str(normalized_workspace_root),
        "requested_workspace_root": str(requested_workspace_root),
        "created_files": created,
        "skipped_files": skipped,
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
    }


def stage_artifact_template(stage: str) -> str:
    sections = STAGE_REQUIRED_SECTIONS[stage]
    upstream_reports = STAGE_UPSTREAM_REPORTS[stage]
    lines = [f"# {STAGE_TITLES[stage]}", ""]
    if not sections:
        return "\n".join(lines + ["待当前任务在该阶段按对象合同补齐。", ""]) + "\n"

    for index, section in enumerate(sections):
        lines.append(f"## {section}")
        if section == "消费的前序产物":
            if upstream_reports:
                lines.extend([f"- `{path}`" for path in upstream_reports])
            else:
                lines.append("- 本阶段无前序正式产物。")
        else:
            lines.append("- 待补齐。")
        if index != len(sections) - 1:
            lines.append("")
    lines.append("")
    return "\n".join(lines)
