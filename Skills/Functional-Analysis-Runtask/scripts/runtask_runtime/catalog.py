from __future__ import annotations

from pathlib import Path
import re

from .types import RuntimeContractPayload, StageChecklistPayload, StageMetadata


SKILL_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = SKILL_ROOT.parents[1]
AI_PROJECTS_ROOT = REPO_ROOT.parent
MANAGED_ROOT_ENV = "FUNCTIONAL_ANALYSIS_RUNTASK_MANAGED_ROOT"
TASK_RUNTIME_ROOT_ENV = "FUNCTIONAL_ANALYSIS_RUNTASK_TASK_RUNTIME_ROOT"
DEFAULT_MANAGED_ROOT = AI_PROJECTS_ROOT / "Human_Work_Zone"
DEFAULT_TASK_RUNTIME_ROOT = AI_PROJECTS_ROOT / "Codex_Skill_Runtime" / "Functional-Analysis-Runtask"
HUMENWORKZONE_COMMANDS = {
    "contract": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json",
    "task_routing": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic task-routing --json",
    "execution_boundary": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json",
    "paths": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json",
}
STAGE_ORDER = [
    "research",
    "architect",
    "preview",
    "design",
    "impact",
    "plan",
    "implementation",
    "validation",
    "final_delivery",
]
STAGE_STATUS_VALUES = {"pending", "in_progress", "blocked", "completed"}
PACKAGE_STATUS_VALUES = {"queued", "active", "blocked", "completed"}
TASK_STATUS_VALUES = {"in_progress", "awaiting_user_selection", "blocked", "closed"}
ACTION_TYPES = {"implementation", "validation", "phase_decision", "state_writeback"}
DESIGN_DECISION_MODES = {"rewrite", "replace", "add"}
REMOTE_PREFIXES = ("http://", "https://")
NUMBERED_SLOT_RE = re.compile(r"^(?P<prefix>\d{3})_(?P<slug>[a-z0-9][a-z0-9_]*)$")

WORKSPACE_LAYOUT = {
    "manifest": "workspace_manifest.yaml",
    "evidence_registry": "research/evidence_registry.yaml",
    "architect_assessment": "architect/assessment.yaml",
    "preview_projection": "preview/projection.yaml",
    "design_decisions": "design/decisions.yaml",
    "impact_map": "impact/impact_map.yaml",
    "milestone_packages": "plan/milestone_packages.yaml",
    "implementation_ledger": "implementation/turn_ledger.yaml",
}

STAGE_ARTIFACTS = {
    "research": "research/001_research_report.md",
    "architect": "architect/001_architecture_assessment_report.md",
    "preview": "preview/001_future_shape_preview.md",
    "design": "design/001_design_strategy.md",
    "impact": "impact/001_impact_investigation.md",
    "plan": WORKSPACE_LAYOUT["milestone_packages"],
    "implementation": WORKSPACE_LAYOUT["implementation_ledger"],
    "validation": "validation/001_acceptance_report.md",
    "final_delivery": "final_delivery/001_final_delivery_brief.md",
}

STAGES: dict[str, StageMetadata] = {
    "research": {
        "purpose": "调研目标项目或目标意图，并落盘调研报告。",
        "entry_requirements": [
            "明确目标意图、目标项目与本地落地对象。",
            "通过 Functional-HumenWorkZone-Manager 解析受管落点。",
            "新任务已经通过 task gate，并已生成 task_runtime.yaml。",
        ],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["evidence_registry"]],
        "required_artifacts": [STAGE_ARTIFACTS["research"]],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            STAGE_ARTIFACTS["research"],
        ],
        "lint_focus": ["manifest/source_assets/evidence_registry", "research report existence"],
    },
    "architect": {
        "purpose": "强制使用 Meta-Architect-MindModel，对当前结构与目标结构给出应/应否评估并落盘。",
        "entry_requirements": ["research 已完成且 research report 可被引用。", "architect 只消费 research 产物。"],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            WORKSPACE_LAYOUT["architect_assessment"],
        ],
        "required_artifacts": [STAGE_ARTIFACTS["research"], STAGE_ARTIFACTS["architect"]],
        "writeback_targets": [WORKSPACE_LAYOUT["architect_assessment"], STAGE_ARTIFACTS["architect"]],
        "lint_focus": ["architect assessment should/should_not", "architect report existence"],
    },
    "preview": {
        "purpose": "强制使用 Meta-Reasoning-Chain，输出未来形态、行为变化、失败模式与回滚阈值。",
        "entry_requirements": ["architect 已完成。", "preview 只消费 research 与 architect 产物。"],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["preview_projection"]],
        "required_artifacts": [STAGE_ARTIFACTS["architect"], STAGE_ARTIFACTS["preview"]],
        "writeback_targets": [WORKSPACE_LAYOUT["preview_projection"], STAGE_ARTIFACTS["preview"]],
        "lint_focus": ["future_shape/behavior_delta/failure_modes/rollback_triggers", "preview report existence"],
    },
    "design": {
        "purpose": "强制使用 Meta-keyword-first-edit，独立落盘优雅实现目标形态的设计方案。",
        "entry_requirements": ["architect 与 preview 已完成。", "design 只消费 research/architect/preview 前序产物。"],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["design_decisions"]],
        "required_artifacts": [STAGE_ARTIFACTS["design"]],
        "writeback_targets": [WORKSPACE_LAYOUT["design_decisions"], STAGE_ARTIFACTS["design"]],
        "lint_focus": ["design decision mode/seamless state", "design report existence"],
    },
    "impact": {
        "purpose": "强制使用 Meta-Impact-Investigation，补齐 direct/indirect/latent/regression 影响面。",
        "entry_requirements": ["design 已完成。", "impact 只消费 research/architect/preview/design 前序产物。"],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["impact_map"]],
        "required_artifacts": [STAGE_ARTIFACTS["impact"]],
        "writeback_targets": [WORKSPACE_LAYOUT["impact_map"], STAGE_ARTIFACTS["impact"]],
        "lint_focus": ["impact map scopes", "impact report existence"],
    },
    "plan": {
        "purpose": "把目标拆成可逐步修改、逐步验证的 milestone package。",
        "entry_requirements": ["impact 已完成。", "plan 只消费 design 与 impact 已落盘产物。"],
        "required_objects": [WORKSPACE_LAYOUT["manifest"], WORKSPACE_LAYOUT["milestone_packages"]],
        "required_artifacts": [STAGE_ARTIFACTS["plan"]],
        "writeback_targets": [WORKSPACE_LAYOUT["milestone_packages"]],
        "lint_focus": ["milestone package fields", "active package uniqueness"],
    },
    "implementation": {
        "purpose": "按 milestone package 逐个实现，并持续回写证据、checklist 与状态裁决。",
        "entry_requirements": ["plan 已存在 active milestone package。", "implementation 只消费 active package 与已声明输入。"],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["milestone_packages"],
            WORKSPACE_LAYOUT["implementation_ledger"],
        ],
        "required_artifacts": [STAGE_ARTIFACTS["implementation"]],
        "writeback_targets": [WORKSPACE_LAYOUT["implementation_ledger"], WORKSPACE_LAYOUT["manifest"]],
        "lint_focus": ["ledger/package/evidence linkage", "implementation evidence completeness"],
    },
    "validation": {
        "purpose": "使用 backend terminal 做真实交互验收，并独立落盘说明如何判定通过。",
        "entry_requirements": ["implementation 已产生真实 ledger 记录。", "validation 只消费前序阶段已落盘产物。"],
        "required_objects": list(WORKSPACE_LAYOUT.values()),
        "required_artifacts": [STAGE_ARTIFACTS["validation"]],
        "writeback_targets": [WORKSPACE_LAYOUT["manifest"], STAGE_ARTIFACTS["validation"]],
        "lint_focus": ["acceptance report existence", "object/document consistency"],
    },
    "final_delivery": {
        "purpose": "最终只向人类输出简要运行报告，因为完整过程已经在文件中落盘。",
        "entry_requirements": ["validation 已完成且 acceptance report 已写回。", "final_delivery 不得新增新的实现或分析。"],
        "required_objects": [WORKSPACE_LAYOUT["manifest"]],
        "required_artifacts": [STAGE_ARTIFACTS["validation"], STAGE_ARTIFACTS["final_delivery"]],
        "writeback_targets": [WORKSPACE_LAYOUT["manifest"], STAGE_ARTIFACTS["final_delivery"]],
        "lint_focus": ["final delivery brief existence", "all stages completed before final delivery closes"],
    },
}


def runtime_contract_payload() -> RuntimeContractPayload:
    from .task_runtime import managed_root, task_runtime_root

    return {
        "status": "ok",
        "skill_name": "Functional-Analysis-Runtask",
        "skill_mode": "executable_workflow_skill",
        "root_shape": ["SKILL.md", "path", "agents", "scripts"],
        "entry_doc": "path/analysis_loop/00_ANALYSIS_LOOP_ENTRY.md",
        "commands": [
            "runtime-contract",
            "read-contract-context",
            "read-path-context",
            "stage-checklist",
            "stage-lint",
            "task-gate-check",
            "task-runtime-scaffold",
            "workspace-scaffold",
        ],
        "stage_order": STAGE_ORDER,
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
        "layout_rule": "小型对象是真相源；阶段正式产物是对外显式交付；每个阶段都只能消费前序已落盘产物或声明允许继承的输入。",
        "compiler_rule": "SKILL.md 只暴露 analysis_loop 入口；下游 markdown 通过 reading_chain 编译完整上下文。",
        "artifact_managed_root": str(managed_root()),
        "task_runtime_root": str(task_runtime_root()),
        "artifact_write_policy": "Task artifacts must first resolve a governed destination through Functional-HumenWorkZone-Manager and must not be written under the skill directory.",
        "task_runtime_policy": "Each task must create a numbered task_runtime.yaml skeleton under Codex_Skill_Runtime before workspace scaffold. New tasks are blocked until prior task runtimes are fully closed.",
        "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
    }


def stage_checklist_payload(stage: str) -> StageChecklistPayload:
    return {
        "stage": stage,
        **STAGES[stage],
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
    }
