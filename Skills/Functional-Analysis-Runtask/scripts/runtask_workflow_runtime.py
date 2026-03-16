from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Any

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
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

STAGES: dict[str, dict[str, Any]] = {
    "research": {
        "purpose": "调研目标项目或目标意图，并落盘调研报告。",
        "entry_requirements": [
            "明确目标意图、目标项目与本地落地对象。",
            "通过 Functional-HumenWorkZone-Manager 解析受管落点。",
            "新任务已经通过 task gate，并已生成 task_runtime.yaml。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["research"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            STAGE_ARTIFACTS["research"],
        ],
        "lint_focus": [
            "manifest/source_assets/evidence_registry",
            "research report existence",
        ],
    },
    "architect": {
        "purpose": "强制使用 Meta-Architect-MindModel，对当前结构与目标结构给出应/应否评估并落盘。",
        "entry_requirements": [
            "research 已完成且 research report 可被引用。",
            "architect 只消费 research 产物。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            WORKSPACE_LAYOUT["architect_assessment"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["research"],
            STAGE_ARTIFACTS["architect"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["architect_assessment"],
            STAGE_ARTIFACTS["architect"],
        ],
        "lint_focus": [
            "architect assessment should/should_not",
            "architect report existence",
        ],
    },
    "preview": {
        "purpose": "强制使用 Meta-Reasoning-Chain，输出未来形态、行为变化、失败模式与回滚阈值。",
        "entry_requirements": [
            "architect 已完成。",
            "preview 只消费 research 与 architect 产物。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["preview_projection"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["architect"],
            STAGE_ARTIFACTS["preview"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["preview_projection"],
            STAGE_ARTIFACTS["preview"],
        ],
        "lint_focus": [
            "future_shape/behavior_delta/failure_modes/rollback_triggers",
            "preview report existence",
        ],
    },
    "design": {
        "purpose": "强制使用 Meta-keyword-first-edit，独立落盘优雅实现目标形态的设计方案。",
        "entry_requirements": [
            "architect 与 preview 已完成。",
            "design 只消费 research/architect/preview 前序产物。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["design_decisions"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["design"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["design_decisions"],
            STAGE_ARTIFACTS["design"],
        ],
        "lint_focus": [
            "design decision mode/seamless state",
            "design report existence",
        ],
    },
    "impact": {
        "purpose": "强制使用 Meta-Impact-Investigation，补齐 direct/indirect/latent/regression 影响面。",
        "entry_requirements": [
            "design 已完成。",
            "impact 只消费 research/architect/preview/design 前序产物。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["impact_map"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["impact"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["impact_map"],
            STAGE_ARTIFACTS["impact"],
        ],
        "lint_focus": [
            "impact map scopes",
            "impact report existence",
        ],
    },
    "plan": {
        "purpose": "把目标拆成可逐步修改、逐步验证的 milestone package。",
        "entry_requirements": [
            "impact 已完成。",
            "plan 只消费 design 与 impact 已落盘产物。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["milestone_packages"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["plan"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["milestone_packages"],
        ],
        "lint_focus": [
            "milestone package fields",
            "active package uniqueness",
        ],
    },
    "implementation": {
        "purpose": "按 milestone package 逐个实现，并持续回写证据、checklist 与状态裁决。",
        "entry_requirements": [
            "plan 已存在 active milestone package。",
            "implementation 只消费 active package 与已声明输入。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["milestone_packages"],
            WORKSPACE_LAYOUT["implementation_ledger"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["implementation"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["implementation_ledger"],
            WORKSPACE_LAYOUT["manifest"],
        ],
        "lint_focus": [
            "ledger/package/evidence linkage",
            "implementation evidence completeness",
        ],
    },
    "validation": {
        "purpose": "使用 backend terminal 做真实交互验收，并独立落盘说明如何判定通过。",
        "entry_requirements": [
            "implementation 已产生真实 ledger 记录。",
            "validation 只消费前序阶段已落盘产物。",
        ],
        "required_objects": list(WORKSPACE_LAYOUT.values()),
        "required_artifacts": [
            STAGE_ARTIFACTS["validation"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            STAGE_ARTIFACTS["validation"],
        ],
        "lint_focus": [
            "acceptance report existence",
            "object/document consistency",
        ],
    },
    "final_delivery": {
        "purpose": "最终只向人类输出简要运行报告，因为完整过程已经在文件中落盘。",
        "entry_requirements": [
            "validation 已完成且 acceptance report 已写回。",
            "final_delivery 不得新增新的实现或分析。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
        ],
        "required_artifacts": [
            STAGE_ARTIFACTS["validation"],
            STAGE_ARTIFACTS["final_delivery"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            STAGE_ARTIFACTS["final_delivery"],
        ],
        "lint_focus": [
            "final delivery brief existence",
            "all stages completed before final delivery closes",
        ],
    },
}


def runtime_contract_payload() -> dict[str, Any]:
    managed_root = _managed_root()
    task_runtime_root = _task_runtime_root()
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
        "artifact_managed_root": str(managed_root),
        "task_runtime_root": str(task_runtime_root),
        "artifact_write_policy": "Task artifacts must first resolve a governed destination through Functional-HumenWorkZone-Manager and must not be written under the skill directory.",
        "task_runtime_policy": "Each task must create a numbered task_runtime.yaml skeleton under Codex_Skill_Runtime before workspace scaffold. New tasks are blocked until prior task runtimes are fully closed.",
        "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
    }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_frontmatter(markdown_path: Path) -> tuple[dict[str, Any], str]:
    text = _read_text(markdown_path)
    if not text.startswith("---\n"):
        return {}, text
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return {}, text
    raw_frontmatter = text[4:closing]
    body = text[closing + 5 :]
    payload = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(payload, dict):
        return {}, body
    return payload, body


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return ""


def _facade_entries(markdown_path: Path) -> list[dict[str, str]]:
    _frontmatter, body = _parse_frontmatter(markdown_path)
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_entries = False
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped == "## 2. 功能入口":
            in_entries = True
            continue
        if in_entries and stripped.startswith("## "):
            break
        if not in_entries:
            continue
        match = re.match(r"^- \[(?P<label>[^\]]+)\][：:]\s*`(?P<target>[^`]+)`", stripped)
        if match:
            current = {
                "key": match.group("label").strip(),
                "target": match.group("target").strip(),
                "hop": "entry",
            }
            items.append(current)
            continue
        if current is None:
            continue
        command_match = re.search(r"--entry\s+([A-Za-z0-9_.-]+)", stripped)
        if command_match:
            current["key"] = command_match.group(1).strip()
    return items


def _reading_chain(markdown_path: Path) -> list[dict[str, str]]:
    if markdown_path.name == "SKILL.md":
        return _facade_entries(markdown_path)
    frontmatter, _body = _parse_frontmatter(markdown_path)
    raw = frontmatter.get("reading_chain")
    if not isinstance(raw, list):
        return []
    items: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        key = item.get("key")
        target = item.get("target")
        hop = item.get("hop")
        if isinstance(key, str) and isinstance(target, str) and isinstance(hop, str):
            items.append({"key": key, "target": target, "hop": hop})
    return items


def compile_reading_chain(entry: str, selection: list[str]) -> dict[str, Any]:
    skill_md = SKILL_ROOT / "SKILL.md"
    resolved_chain = ["SKILL.md"]
    _frontmatter, skill_body = _parse_frontmatter(skill_md)
    segments: list[dict[str, str]] = [
        {"source": "SKILL.md", "title": _extract_title(skill_body), "content": skill_body.strip()}
    ]
    root_items = _reading_chain(skill_md)
    chosen = next((item for item in root_items if item["key"] == entry), None)
    if chosen is None:
        return {
            "status": "error",
            "error": "entry_not_found",
            "entry": entry,
            "available_entries": [item["key"] for item in root_items],
        }
    queue = list(selection)
    current = (skill_md.parent / chosen["target"]).resolve()
    while True:
        _frontmatter, body = _parse_frontmatter(current)
        relative = current.relative_to(SKILL_ROOT).as_posix()
        resolved_chain.append(relative)
        segments.append({"source": relative, "title": _extract_title(body), "content": body.strip()})
        items = _reading_chain(current)
        if not items:
            break
        if len(items) > 1:
            requested = queue.pop(0) if queue else None
            if requested is None:
                return {
                    "status": "branch_selection_required",
                    "entry": entry,
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item["key"] for item in items],
                    "current_source": relative,
                }
            chosen = next((item for item in items if item["key"] == requested), None)
            if chosen is None:
                return {
                    "status": "branch_selection_required",
                    "entry": entry,
                    "resolved_chain": resolved_chain,
                    "segments": segments,
                    "available_next": [item["key"] for item in items],
                    "current_source": relative,
                }
        else:
            chosen = items[0]
        current = (current.parent / chosen["target"]).resolve()
    return {
        "status": "ok",
        "entry": entry,
        "resolved_chain": resolved_chain,
        "segments": segments,
        "compiled_markdown": "\n\n".join(item["content"] for item in segments if item["content"]),
    }


def stage_checklist_payload(stage: str) -> dict[str, Any]:
    return {
        "stage": stage,
        **STAGES[stage],
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
    }


def scaffold_workspace(workspace_root: Path, force: bool = False) -> dict[str, Any]:
    requested_workspace_root = workspace_root.resolve()
    boundary_error = _workspace_root_boundary_error(requested_workspace_root)
    if boundary_error is not None:
        return boundary_error
    workspace_root = _normalize_numbered_workspace_root(requested_workspace_root)
    if not workspace_root.exists():
        gate_payload = task_gate_check_payload()
        if gate_payload["status"] != "ok":
            return {
                "status": "fail",
                "reason": "unfinished_task_exists",
                "workspace_root": str(workspace_root),
                "requested_workspace_root": str(requested_workspace_root),
                "task_runtime_root": gate_payload["task_runtime_root"],
                "open_tasks": gate_payload["open_tasks"],
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
            "should_change": [],
            "should_not_change": [],
            "architecture_judgement": "",
        },
        WORKSPACE_LAYOUT["preview_projection"]: {
            "future_shape": [],
            "behavior_delta": [],
            "failure_modes": [],
            "rollback_triggers": [],
        },
        WORKSPACE_LAYOUT["design_decisions"]: {
            "decision_mode": "rewrite",
            "seamless_state": "",
            "decision_items": [],
        },
        WORKSPACE_LAYOUT["impact_map"]: {
            "task_mode": "WRITE_INTENT",
            "direct_scope": [],
            "indirect_scope": [],
            "latent_related": [],
            "validation_or_evidence": [],
            "must_update": [],
            "must_check_before_edit": [],
            "regression_surface": [],
        },
        WORKSPACE_LAYOUT["milestone_packages"]: {"milestone_packages": []},
        WORKSPACE_LAYOUT["implementation_ledger"]: {"entries": []},
    }
    created: list[str] = []
    skipped: list[str] = []
    for relative, payload in objects.items():
        target = workspace_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(relative)
            continue
        target.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(relative)
    for stage, relative in STAGE_ARTIFACTS.items():
        target = workspace_root / relative
        if target.suffix != ".md":
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(relative)
            continue
        target.write_text(_stage_artifact_template(stage), encoding="utf-8")
        created.append(relative)
    return {
        "status": "ok",
        "workspace_root": str(workspace_root),
        "requested_workspace_root": str(requested_workspace_root),
        "created_files": created,
        "skipped_files": skipped,
        "workspace_layout": WORKSPACE_LAYOUT,
        "stage_artifacts": STAGE_ARTIFACTS,
    }


def stage_lint_payload(workspace_root: Path, stage: str) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    boundary_error = _workspace_root_boundary_error(workspace_root)
    if boundary_error is not None:
        boundary_error["stage"] = stage
        boundary_error["workspace_root"] = str(workspace_root)
        boundary_error["checked_files"] = _checked_files_payload(workspace_root)
        return boundary_error
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    loaded = _load_workspace(workspace_root, errors)
    if not loaded:
        return {
            "status": "fail",
            "stage": stage,
            "workspace_root": str(workspace_root),
            "errors": errors,
            "warnings": warnings,
            "checked_files": _checked_files_payload(workspace_root),
        }

    manifest = loaded["manifest"]
    source_asset_ids = _validate_manifest(workspace_root, manifest, errors, warnings)
    evidence_ids = _validate_evidence_registry(workspace_root, loaded["evidence_registry"], errors, warnings)

    if stage in {"architect", "preview", "design", "impact", "plan", "implementation", "validation", "final_delivery", "all"}:
        _validate_architect_assessment(loaded["architect_assessment"], errors)
        _validate_preview_projection(loaded["preview_projection"], errors)
        _validate_design_decisions(loaded["design_decisions"], errors)
        _validate_impact_map(loaded["impact_map"], errors)

    package_ids, active_package_ids, completed_package_ids = set(), [], []
    if stage in {"plan", "implementation", "validation", "final_delivery", "all"}:
        package_ids, active_package_ids, completed_package_ids = _validate_milestone_packages(
            loaded["milestone_packages"],
            errors,
        )

    if stage in {"implementation", "validation", "final_delivery", "all"}:
        _validate_implementation_ledger(
            workspace_root,
            loaded["implementation_ledger"],
            package_ids,
            evidence_ids,
            errors,
        )
        _validate_completed_packages_have_witness(
            loaded["implementation_ledger"],
            completed_package_ids,
            errors,
        )

    _validate_stage_artifacts(workspace_root, manifest, stage, errors)
    _validate_stage_consistency(
        workspace_root,
        manifest,
        stage,
        active_package_ids,
        loaded["implementation_ledger"],
        errors,
        warnings,
    )

    return {
        "status": "pass" if not errors else "fail",
        "stage": stage,
        "workspace_root": str(workspace_root),
        "errors": errors,
        "warnings": warnings,
        "checked_files": _checked_files_payload(workspace_root),
    }


def _checked_files_payload(workspace_root: Path) -> dict[str, str]:
    payload = {key: str((workspace_root / value).resolve()) for key, value in WORKSPACE_LAYOUT.items()}
    for stage, relative in STAGE_ARTIFACTS.items():
        payload[f"artifact_{stage}"] = str((workspace_root / relative).resolve())
    return payload


def _load_workspace(workspace_root: Path, errors: list[dict[str, str]]) -> dict[str, Any]:
    loaded: dict[str, Any] = {}
    for key, relative in WORKSPACE_LAYOUT.items():
        target = workspace_root / relative
        if not target.exists():
            _error(errors, "missing_file", relative, f"缺少必需对象文件：{relative}")
            continue
        try:
            payload = yaml.safe_load(target.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            _error(errors, "yaml_parse_error", relative, f"YAML 解析失败：{exc}")
            continue
        if not isinstance(payload, dict):
            _error(errors, "invalid_root_type", relative, "对象根节点必须是映射。")
            continue
        loaded[key] = payload
    return loaded


def _managed_root() -> Path:
    return Path(__import__("os").environ.get(MANAGED_ROOT_ENV, str(DEFAULT_MANAGED_ROOT))).expanduser().resolve()


def _task_runtime_root() -> Path:
    return Path(__import__("os").environ.get(TASK_RUNTIME_ROOT_ENV, str(DEFAULT_TASK_RUNTIME_ROOT))).expanduser().resolve()


def _is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def _workspace_root_boundary_error(workspace_root: Path) -> dict[str, Any] | None:
    managed_root = _managed_root()
    if _is_relative_to(workspace_root, SKILL_ROOT):
        return {
            "status": "fail",
            "reason": "workspace_root_forbidden_under_skill_root",
            "workspace_root": str(workspace_root),
            "managed_root": str(managed_root),
            "message": "任务产物不得落到 Functional-Analysis-Runtask 技能目录内部；请先通过 Functional-HumenWorkZone-Manager 解析 Human_Work_Zone 受管落点。",
            "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
        }
    if not _is_relative_to(workspace_root, managed_root):
        return {
            "status": "fail",
            "reason": "workspace_root_must_be_under_managed_root",
            "workspace_root": str(workspace_root),
            "managed_root": str(managed_root),
            "message": "workspace_root 必须位于 Human_Work_Zone 受管根下；请先通过 Functional-HumenWorkZone-Manager 解析目标分区。",
            "artifact_handoff_commands": HUMENWORKZONE_COMMANDS,
        }
    return None


def task_gate_check_payload(task_runtime_root: Path | None = None) -> dict[str, Any]:
    runtime_root = (task_runtime_root or _task_runtime_root()).resolve()
    open_tasks: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if runtime_root.exists():
        for _prefix, _slug, task_dir in _numbered_slot_entries(runtime_root):
            runtime_file = task_dir / "task_runtime.yaml"
            if not runtime_file.exists():
                open_tasks.append(
                    {
                        "task_root": str(task_dir),
                        "reason": "missing_task_runtime_file",
                        "resume_hint": "补齐 task_runtime.yaml 后再继续。",
                    }
                )
                continue
            try:
                payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8"))
            except yaml.YAMLError as exc:
                open_tasks.append(
                    {
                        "task_root": str(task_dir),
                        "reason": "task_runtime_yaml_parse_error",
                        "detail": str(exc),
                        "resume_hint": "修复 task_runtime.yaml 后再继续。",
                    }
                )
                continue
            if not isinstance(payload, dict):
                open_tasks.append(
                    {
                        "task_root": str(task_dir),
                        "reason": "invalid_task_runtime_root_type",
                        "resume_hint": "task_runtime.yaml 根节点必须是映射。",
                    }
                )
                continue
            if _task_runtime_is_closed(payload):
                continue
            open_tasks.append(
                {
                    "task_root": str(task_dir),
                    "task_id": payload.get("task_id", ""),
                    "task_status": payload.get("task_status", ""),
                    "current_stage": payload.get("current_stage", ""),
                    "current_step": payload.get("current_step", ""),
                    "ended_stage": payload.get("ended_stage", ""),
                    "ended_step": payload.get("ended_step", ""),
                    "resume_hint": payload.get("resume_hint", "继续推进当前 task_runtime.yaml，直至全部阶段完成并 closed。"),
                }
            )
    if not runtime_root.exists():
        warnings.append({"code": "task_runtime_root_missing", "message": "task runtime root 尚未创建；当前允许启动首个任务。"})
    return {
        "status": "ok" if not open_tasks else "fail",
        "reason": "" if not open_tasks else "unfinished_task_exists",
        "task_runtime_root": str(runtime_root),
        "open_tasks": open_tasks,
        "warnings": warnings,
    }


def task_runtime_scaffold(task_name: str, workspace_root: Path | None = None, force: bool = False) -> dict[str, Any]:
    runtime_root = _task_runtime_root()
    resolved_workspace_root = _resolve_task_workspace_root(task_name, workspace_root, runtime_root)
    boundary_error = _workspace_root_boundary_error(resolved_workspace_root)
    if boundary_error is not None:
        return boundary_error
    slug = _slugify(task_name)
    prefix = _resolve_shared_numbered_prefix(runtime_root, resolved_workspace_root.parent, slug)
    task_dir = runtime_root / f"{prefix}_{slug}"
    runtime_file = task_dir / "task_runtime.yaml"
    if runtime_file.exists() and not force:
        payload = yaml.safe_load(runtime_file.read_text(encoding="utf-8")) or {}
        return {
            "status": "ok",
            "task_root": str(task_dir),
            "task_runtime_file": str(runtime_file),
            "task_id": payload.get("task_id", f"{prefix}_{slug}"),
            "task_runtime_root": str(runtime_root),
            "workspace_root": payload.get("workspace_root", str(resolved_workspace_root)),
            "reused_existing": True,
        }
    gate_payload = task_gate_check_payload(runtime_root)
    if gate_payload["status"] != "ok":
        return gate_payload
    task_dir.mkdir(parents=True, exist_ok=True)
    resolved_workspace_root.mkdir(parents=True, exist_ok=True)
    payload = _task_runtime_template(
        task_id=f"{prefix}_{slug}",
        task_name=task_name,
        task_slug=slug,
        workspace_root=resolved_workspace_root,
    )
    runtime_file.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {
        "status": "ok",
        "task_root": str(task_dir),
        "task_runtime_file": str(runtime_file),
        "task_id": payload["task_id"],
        "task_runtime_root": str(runtime_root),
        "workspace_root": str(resolved_workspace_root),
        "reused_existing": False,
    }


def _validate_manifest(
    workspace_root: Path,
    manifest: dict[str, Any],
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> set[str]:
    source = WORKSPACE_LAYOUT["manifest"]
    source_asset_ids: set[str] = set()
    required_keys = [
        "analysis_id",
        "intent_summary",
        "execution_mode",
        "current_stage",
        "source_assets",
        "target_scope",
        "stage_status",
        "stage_outputs",
        "writeback_status",
    ]
    for key in required_keys:
        if key not in manifest:
            _error(errors, "missing_field", source, f"manifest 缺少字段：{key}")
    if manifest.get("execution_mode") not in {"continuous", "single_stage"}:
        _error(errors, "invalid_execution_mode", source, "execution_mode 只能是 continuous 或 single_stage。")
    if manifest.get("current_stage") not in STAGE_ORDER:
        _error(errors, "invalid_current_stage", source, "current_stage 不在固定阶段列表内。")
    if manifest.get("execution_mode") == "single_stage":
        focus = manifest.get("single_stage_focus")
        if focus not in STAGE_ORDER:
            _error(errors, "invalid_single_stage_focus", source, "single_stage 模式必须声明有效的 single_stage_focus。")
    stage_status = manifest.get("stage_status")
    if not isinstance(stage_status, dict):
        _error(errors, "invalid_stage_status", source, "stage_status 必须是映射。")
        stage_status = {}
    for stage in STAGE_ORDER:
        value = stage_status.get(stage)
        if value not in STAGE_STATUS_VALUES:
            _error(errors, "invalid_stage_value", source, f"{stage} 的状态必须属于 {sorted(STAGE_STATUS_VALUES)}。")
    stage_outputs = manifest.get("stage_outputs")
    if not isinstance(stage_outputs, dict):
        _error(errors, "invalid_stage_outputs", source, "stage_outputs 必须是映射。")
        stage_outputs = {}
    for stage in STAGE_ORDER:
        output_path = stage_outputs.get(stage)
        if not isinstance(output_path, str) or not output_path:
            _error(errors, "missing_stage_output", source, f"缺少阶段产物路径：{stage}")
            continue
        resolved = _resolve_local_path(output_path, workspace_root)
        if resolved is not None and not resolved.exists():
            _error(errors, "missing_stage_output_target", source, f"{stage} 产物路径不存在：{resolved}")
    source_assets = manifest.get("source_assets")
    if not isinstance(source_assets, list):
        _error(errors, "invalid_source_assets", source, "source_assets 必须是列表。")
        source_assets = []
    for index, asset in enumerate(source_assets):
        item_source = f"{source}:source_assets[{index}]"
        if not isinstance(asset, dict):
            _error(errors, "invalid_asset_item", item_source, "source asset 必须是映射。")
            continue
        asset_id = asset.get("asset_id")
        asset_path = asset.get("path")
        role = asset.get("role")
        if not isinstance(asset_id, str) or not asset_id:
            _error(errors, "missing_asset_id", item_source, "source asset 缺少 asset_id。")
        elif asset_id in source_asset_ids:
            _error(errors, "duplicate_asset_id", item_source, f"重复的 asset_id：{asset_id}")
        else:
            source_asset_ids.add(asset_id)
        if not isinstance(role, str) or not role:
            _error(errors, "missing_asset_role", item_source, "source asset 缺少 role。")
        if not isinstance(asset_path, str) or not asset_path:
            _error(errors, "missing_asset_path", item_source, "source asset 缺少 path。")
        else:
            resolved = _resolve_local_path(asset_path, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_asset_path_target", item_source, f"source asset 路径不存在：{resolved}")
    if not source_assets:
        _warning(warnings, "empty_source_assets", source, "source_assets 为空；research 未完成。")
    return source_asset_ids


def _validate_evidence_registry(
    workspace_root: Path,
    evidence_registry: dict[str, Any],
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> set[str]:
    source = WORKSPACE_LAYOUT["evidence_registry"]
    evidence_items = evidence_registry.get("evidence_items")
    evidence_ids: set[str] = set()
    if not isinstance(evidence_items, list):
        _error(errors, "invalid_evidence_items", source, "evidence_items 必须是列表。")
        return evidence_ids
    for index, item in enumerate(evidence_items):
        item_source = f"{source}:evidence_items[{index}]"
        if not isinstance(item, dict):
            _error(errors, "invalid_evidence_item", item_source, "evidence item 必须是映射。")
            continue
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            _error(errors, "missing_evidence_id", item_source, "evidence item 缺少 evidence_id。")
        elif evidence_id in evidence_ids:
            _error(errors, "duplicate_evidence_id", item_source, f"重复的 evidence_id：{evidence_id}")
        else:
            evidence_ids.add(evidence_id)
        for field in ("kind", "location", "relevance", "supports"):
            if field not in item:
                _error(errors, "missing_evidence_field", item_source, f"evidence item 缺少字段：{field}")
        location = item.get("location")
        if isinstance(location, str) and location:
            resolved = _resolve_local_path(location, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_evidence_target", item_source, f"evidence 路径不存在：{resolved}")
        supports = item.get("supports")
        if supports is not None and not isinstance(supports, list):
            _error(errors, "invalid_evidence_supports", item_source, "supports 必须是列表。")
    if not evidence_items:
        _warning(warnings, "empty_evidence_registry", source, "evidence registry 为空；research 未完成。")
    return evidence_ids


def _validate_architect_assessment(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["architect_assessment"]
    if not isinstance(payload.get("should_change"), list):
        _error(errors, "invalid_should_change", source, "should_change 必须是列表。")
    if not isinstance(payload.get("should_not_change"), list):
        _error(errors, "invalid_should_not_change", source, "should_not_change 必须是列表。")
    if not isinstance(payload.get("architecture_judgement"), str):
        _error(errors, "invalid_architecture_judgement", source, "architecture_judgement 必须是字符串。")


def _validate_preview_projection(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["preview_projection"]
    for field in ("future_shape", "behavior_delta", "failure_modes", "rollback_triggers"):
        if not isinstance(payload.get(field), list):
            _error(errors, "invalid_preview_field", source, f"{field} 必须是列表。")


def _validate_design_decisions(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["design_decisions"]
    if payload.get("decision_mode") not in DESIGN_DECISION_MODES:
        _error(errors, "invalid_decision_mode", source, f"decision_mode 必须属于 {sorted(DESIGN_DECISION_MODES)}。")
    if not isinstance(payload.get("seamless_state"), str):
        _error(errors, "invalid_seamless_state", source, "seamless_state 必须是字符串。")
    decision_items = payload.get("decision_items")
    if not isinstance(decision_items, list):
        _error(errors, "invalid_decision_items", source, "decision_items 必须是列表。")
        return
    for index, item in enumerate(decision_items):
        item_source = f"{source}:decision_items[{index}]"
        if not isinstance(item, dict):
            _error(errors, "invalid_design_item", item_source, "decision item 必须是映射。")
            continue
        for field in ("title", "rationale"):
            if not isinstance(item.get(field), str) or not item.get(field):
                _error(errors, "missing_design_item_field", item_source, f"缺少字段：{field}")


def _validate_impact_map(payload: dict[str, Any], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["impact_map"]
    if payload.get("task_mode") not in {"READ_ONLY", "WRITE_INTENT"}:
        _error(errors, "invalid_task_mode", source, "task_mode 必须是 READ_ONLY 或 WRITE_INTENT。")
    for field in (
        "direct_scope",
        "indirect_scope",
        "latent_related",
        "validation_or_evidence",
        "must_update",
        "must_check_before_edit",
        "regression_surface",
    ):
        if not isinstance(payload.get(field), list):
            _error(errors, "invalid_impact_field", source, f"{field} 必须是列表。")


def _validate_milestone_packages(
    payload: dict[str, Any],
    errors: list[dict[str, str]],
) -> tuple[set[str], list[str], list[str]]:
    source = WORKSPACE_LAYOUT["milestone_packages"]
    packages = payload.get("milestone_packages")
    package_ids: set[str] = set()
    active_ids: list[str] = []
    completed_ids: list[str] = []
    if not isinstance(packages, list):
        _error(errors, "invalid_milestone_packages", source, "milestone_packages 必须是列表。")
        return package_ids, active_ids, completed_ids
    for index, item in enumerate(packages):
        item_source = f"{source}:milestone_packages[{index}]"
        if not isinstance(item, dict):
            _error(errors, "invalid_package_item", item_source, "milestone package 必须是映射。")
            continue
        package_id = item.get("package_id")
        if not isinstance(package_id, str) or not package_id:
            _error(errors, "missing_package_id", item_source, "package 缺少 package_id。")
        elif package_id in package_ids:
            _error(errors, "duplicate_package_id", item_source, f"重复的 package_id：{package_id}")
        else:
            package_ids.add(package_id)
        for field in ("goal", "consumes", "delivers", "validation", "status"):
            if field not in item:
                _error(errors, "missing_package_field", item_source, f"package 缺少字段：{field}")
        status = item.get("status")
        if status not in PACKAGE_STATUS_VALUES:
            _error(errors, "invalid_package_status", item_source, f"package.status 必须属于 {sorted(PACKAGE_STATUS_VALUES)}。")
        elif status == "active" and isinstance(package_id, str) and package_id:
            active_ids.append(package_id)
        elif status == "completed" and isinstance(package_id, str) and package_id:
            completed_ids.append(package_id)
    if len(active_ids) > 1:
        _error(errors, "multiple_active_packages", source, "同一时刻只能存在 1 个 active milestone package。")
    return package_ids, active_ids, completed_ids


def _validate_implementation_ledger(
    workspace_root: Path,
    payload: dict[str, Any],
    package_ids: set[str],
    evidence_ids: set[str],
    errors: list[dict[str, str]],
) -> None:
    source = WORKSPACE_LAYOUT["implementation_ledger"]
    entries = payload.get("entries")
    if not isinstance(entries, list):
        _error(errors, "invalid_entries", source, "entries 必须是列表。")
        return
    seen_entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        item_source = f"{source}:entries[{index}]"
        if not isinstance(entry, dict):
            _error(errors, "invalid_entry_item", item_source, "ledger entry 必须是映射。")
            continue
        entry_id = entry.get("entry_id")
        if not isinstance(entry_id, str) or not entry_id:
            _error(errors, "missing_entry_id", item_source, "ledger entry 缺少 entry_id。")
        elif entry_id in seen_entry_ids:
            _error(errors, "duplicate_entry_id", item_source, f"重复的 entry_id：{entry_id}")
        else:
            seen_entry_ids.add(entry_id)
        package_id = entry.get("package_id")
        if not isinstance(package_id, str) or package_id not in package_ids:
            _error(errors, "invalid_entry_package_id", item_source, f"ledger entry 必须引用有效 package_id：{package_id}")
        for field in ("action_types", "summary", "changed_paths", "validation_runs", "evidence_refs", "status_updates", "residual_issues"):
            if field not in entry:
                _error(errors, "missing_entry_field", item_source, f"ledger entry 缺少字段：{field}")
        action_types = entry.get("action_types", [])
        if not isinstance(action_types, list):
            _error(errors, "invalid_action_types", item_source, "action_types 必须是列表。")
            action_types = []
        for action in action_types:
            if action not in ACTION_TYPES:
                _error(errors, "invalid_action_type", item_source, f"未知 action_type：{action}")
        changed_paths = entry.get("changed_paths", [])
        if not isinstance(changed_paths, list):
            _error(errors, "invalid_changed_paths", item_source, "changed_paths 必须是列表。")
            changed_paths = []
        for raw_path in changed_paths:
            if not isinstance(raw_path, str) or not raw_path:
                _error(errors, "invalid_changed_path_item", item_source, "changed_paths 中只能包含非空字符串。")
                continue
            resolved = _resolve_local_path(raw_path, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_changed_path", item_source, f"changed_paths 指向的路径不存在：{resolved}")
        validation_runs = entry.get("validation_runs", [])
        if not isinstance(validation_runs, list):
            _error(errors, "invalid_validation_runs", item_source, "validation_runs 必须是列表。")
            validation_runs = []
        for run in validation_runs:
            if not isinstance(run, dict):
                _error(errors, "invalid_validation_run", item_source, "validation run 必须是映射。")
                continue
            if not isinstance(run.get("command"), str) or not run.get("command"):
                _error(errors, "missing_validation_command", item_source, "validation run 缺少 command。")
            if not isinstance(run.get("result"), str) or not run.get("result"):
                _error(errors, "missing_validation_result", item_source, "validation run 缺少 result。")
        evidence_refs = entry.get("evidence_refs", [])
        if not isinstance(evidence_refs, list):
            _error(errors, "invalid_entry_evidence_refs", item_source, "evidence_refs 必须是列表。")
            evidence_refs = []
        for ref in evidence_refs:
            if ref not in evidence_ids:
                _error(errors, "invalid_entry_evidence_ref", item_source, f"未找到 evidence ref：{ref}")
        requires_evidence = bool(set(action_types) & ACTION_TYPES) or bool(changed_paths) or bool(validation_runs)
        if requires_evidence and not evidence_refs:
            _error(errors, "missing_entry_evidence", item_source, "发生真实实现、验证或状态写回时，evidence_refs 不得为空。")


def _validate_completed_packages_have_witness(
    payload: dict[str, Any],
    completed_package_ids: list[str],
    errors: list[dict[str, str]],
) -> None:
    if not completed_package_ids:
        return
    entries = payload.get("entries", [])
    for package_id in completed_package_ids:
        has_witness = False
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("package_id") != package_id:
                continue
            if entry.get("validation_runs") and entry.get("evidence_refs"):
                has_witness = True
                break
        if not has_witness:
            _error(
                errors,
                "completed_package_without_witness",
                WORKSPACE_LAYOUT["implementation_ledger"],
                f"已完成 package {package_id} 没有对应验证与证据记录。",
            )


def _validate_stage_artifacts(
    workspace_root: Path,
    manifest: dict[str, Any],
    requested_stage: str,
    errors: list[dict[str, str]],
) -> None:
    stage_outputs = manifest.get("stage_outputs", {})
    stages_to_check = STAGE_ORDER if requested_stage == "all" else [requested_stage]
    for stage in stages_to_check:
        output_path = stage_outputs.get(stage, STAGE_ARTIFACTS[stage])
        if not isinstance(output_path, str) or not output_path:
            _error(errors, "missing_stage_output", WORKSPACE_LAYOUT["manifest"], f"缺少阶段产物声明：{stage}")
            continue
        resolved = _resolve_local_path(output_path, workspace_root)
        if resolved is not None and not resolved.exists():
            _error(errors, "missing_stage_output_target", WORKSPACE_LAYOUT["manifest"], f"{stage} 产物不存在：{resolved}")


def _validate_stage_consistency(
    workspace_root: Path,
    manifest: dict[str, Any],
    requested_stage: str,
    active_package_ids: list[str],
    ledger_payload: dict[str, Any],
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> None:
    source = WORKSPACE_LAYOUT["manifest"]
    stage_status = manifest.get("stage_status", {})
    current_stage = manifest.get("current_stage")
    execution_mode = manifest.get("execution_mode")
    if execution_mode == "continuous" and current_stage in STAGE_ORDER:
        current_index = STAGE_ORDER.index(current_stage)
        for index, stage in enumerate(STAGE_ORDER):
            if index < current_index and stage_status.get(stage) != "completed":
                _error(errors, "incomplete_previous_stage", source, f"连续执行模式下，前置阶段 {stage} 必须是 completed。")
    if requested_stage in {"plan", "implementation", "validation", "final_delivery", "all"}:
        if stage_status.get("plan") in {"in_progress", "completed"} and len(active_package_ids) > 1:
            _error(errors, "invalid_active_package_count", source, "plan/implementation 阶段不允许多个 active package。")
    if requested_stage in {"implementation", "validation", "final_delivery", "all"}:
        implementation_status = stage_status.get("implementation")
        entries = ledger_payload.get("entries", [])
        if implementation_status in {"in_progress", "completed"} and not entries:
            _error(errors, "implementation_without_ledger", source, "implementation 已启动，但 ledger 为空。")
        if implementation_status == "in_progress" and not active_package_ids:
            _error(errors, "implementation_without_active_package", source, "implementation 进行中时必须存在 active milestone package。")
    if requested_stage in {"validation", "final_delivery", "all"}:
        current_sync_report = manifest.get("writeback_status", {}).get("current_sync_report")
        if not isinstance(current_sync_report, str) or not current_sync_report:
            _error(errors, "missing_current_sync_report", source, "validation/final_delivery 要求声明 current_sync_report。")
        else:
            resolved = _resolve_local_path(current_sync_report, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_current_sync_report_path", source, f"current_sync_report 路径不存在：{resolved}")
    if requested_stage in {"final_delivery", "all"} and stage_status.get("final_delivery") == "completed":
        final_delivery_brief = manifest.get("writeback_status", {}).get("final_delivery_brief")
        if not isinstance(final_delivery_brief, str) or not final_delivery_brief:
            _error(errors, "missing_final_delivery_brief", source, "final_delivery 完成时必须声明 final_delivery_brief。")
        else:
            resolved = _resolve_local_path(final_delivery_brief, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_final_delivery_brief_path", source, f"final_delivery_brief 路径不存在：{resolved}")
        for stage in STAGE_ORDER:
            if stage_status.get(stage) != "completed":
                _error(errors, "final_delivery_completed_but_stage_open", source, f"final_delivery 已完成，但 {stage} 不是 completed。")
    if stage_status.get("validation") == "pending" and requested_stage == "validation":
        _warning(warnings, "validation_not_started", source, "当前在 validation 阶段执行 lint，但 manifest 仍标记为 pending。")


def _resolve_local_path(raw_path: str, workspace_root: Path) -> Path | None:
    if raw_path.startswith(REMOTE_PREFIXES):
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = workspace_root / path
    return path.resolve()


def _task_runtime_is_closed(payload: dict[str, Any]) -> bool:
    if payload.get("task_status") != "closed":
        return False
    if payload.get("ended_stage") != "final_delivery":
        return False
    stages = payload.get("stages")
    if not isinstance(stages, dict):
        return False
    for stage in STAGE_ORDER:
        stage_payload = stages.get(stage)
        if not isinstance(stage_payload, dict):
            return False
        if stage_payload.get("status") != "completed":
            return False
    return True


def _task_runtime_template(
    task_id: str,
    task_name: str,
    task_slug: str,
    workspace_root: Path | None,
) -> dict[str, Any]:
    timestamp = datetime.now(timezone.utc).isoformat()
    stages: dict[str, Any] = {}
    for index, stage in enumerate(STAGE_ORDER):
        stages[stage] = {
            "status": "in_progress" if index == 0 else "pending",
            "checklist": [],
        }
    return {
        "task_id": task_id,
        "task_name": task_name,
        "task_slug": task_slug,
        "task_status": "in_progress",
        "workspace_root": "" if workspace_root is None else str(workspace_root.resolve()),
        "created_at": timestamp,
        "updated_at": timestamp,
        "current_stage": "research",
        "current_step": "",
        "ended_stage": "",
        "ended_step": "",
        "ended_reason": "",
        "resume_hint": "从 current_stage/current_step 指向的位置继续推进。",
        "stages": stages,
    }


def _slugify(raw: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", raw.strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "task"


def _numbered_slot_entries(root: Path) -> list[tuple[int, str, Path]]:
    if not root.exists():
        return []
    entries: list[tuple[int, str, Path]] = []
    for item in root.iterdir():
        if not item.is_dir():
            continue
        parsed = _parse_numbered_slot_name(item.name)
        if parsed is None:
            continue
        prefix, slug = parsed
        entries.append((prefix, slug, item))
    return sorted(entries, key=lambda entry: (entry[0], entry[1], entry[2].name))


def _parse_numbered_slot_name(name: str) -> tuple[int, str] | None:
    match = NUMBERED_SLOT_RE.match(name)
    if match is None:
        return None
    return int(match.group("prefix")), match.group("slug")


def _highest_numbered_prefix(root: Path) -> int:
    highest = 0
    for prefix, _slug, _path in _numbered_slot_entries(root):
        highest = max(highest, prefix)
    return highest


def _matching_numbered_prefixes(root: Path, slug: str) -> list[int]:
    return [prefix for prefix, entry_slug, _path in _numbered_slot_entries(root) if entry_slug == slug]


def _resolve_shared_numbered_prefix(runtime_root: Path, workspace_container: Path, slug: str) -> str:
    matches = _matching_numbered_prefixes(runtime_root, slug) + _matching_numbered_prefixes(workspace_container, slug)
    if matches:
        return f"{min(matches):03d}"
    next_prefix = max(_highest_numbered_prefix(runtime_root), _highest_numbered_prefix(workspace_container)) + 1
    return f"{next_prefix:03d}"


def _normalize_numbered_workspace_root(workspace_root: Path) -> Path:
    workspace_root = workspace_root.resolve()
    boundary_error = _workspace_root_boundary_error(workspace_root)
    if boundary_error is not None:
        return workspace_root
    parsed = _parse_numbered_slot_name(workspace_root.name)
    if parsed is not None:
        return workspace_root
    slug = _slugify(workspace_root.name)
    container = workspace_root.parent
    matches = [path for _prefix, entry_slug, path in _numbered_slot_entries(container) if entry_slug == slug]
    if matches:
        return matches[0]
    next_prefix = _highest_numbered_prefix(container) + 1
    return container / f"{next_prefix:03d}_{slug}"


def _resolve_task_workspace_root(task_name: str, workspace_root: Path | None, runtime_root: Path) -> Path:
    task_slug = _slugify(task_name)
    if workspace_root is None:
        container = (_managed_root() / "Temporary_Files").resolve()
    else:
        requested_workspace_root = workspace_root.resolve()
        boundary_error = _workspace_root_boundary_error(requested_workspace_root)
        if boundary_error is not None:
            return requested_workspace_root
        container = requested_workspace_root.parent
    prefix = _resolve_shared_numbered_prefix(runtime_root, container, task_slug)
    return container / f"{prefix}_{task_slug}"


def _stage_artifact_template(stage: str) -> str:
    title_map = {
        "research": "Research Report",
        "architect": "Architecture Assessment Report",
        "preview": "Future Shape Preview",
        "design": "Design Strategy",
        "impact": "Impact Investigation",
        "validation": "Acceptance Report",
        "final_delivery": "Final Delivery Brief",
    }
    return f"# {title_map[stage]}\n\n待当前任务在 `{stage}` 阶段补齐。\n"


def _error(errors: list[dict[str, str]], code: str, source: str, message: str) -> None:
    errors.append({"code": code, "source": source, "message": message})


def _warning(warnings: list[dict[str, str]], code: str, source: str, message: str) -> None:
    warnings.append({"code": code, "source": source, "message": message})
