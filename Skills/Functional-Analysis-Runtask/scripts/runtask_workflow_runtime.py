from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
STAGE_ORDER = [
    "research_baseline",
    "architecture_convergence",
    "plan",
    "implementation",
    "validation",
]
STAGE_STATUS_VALUES = {"pending", "in_progress", "blocked", "completed"}
SLICE_STATUS_VALUES = {"queued", "active", "blocked", "completed"}
ACTION_TYPES = {"implementation", "validation", "phase_decision", "state_writeback"}
REMOTE_PREFIXES = ("http://", "https://")

WORKSPACE_LAYOUT = {
    "manifest": "workspace_manifest.yaml",
    "evidence_registry": "research/evidence_registry.yaml",
    "architecture_decisions": "design/architecture_decisions.yaml",
    "plan_slices": "plan/slices.yaml",
    "implementation_ledger": "implementation/turn_ledger.yaml",
}

STAGES: dict[str, dict[str, Any]] = {
    "research_baseline": {
        "purpose": "锁定目标意图或目标项目、本地落地目标、来源资产与高信噪比证据入口。",
        "entry_requirements": [
            "明确本轮目标意图、目标项目或目标实现对象。",
            "识别当前应继承的旧资产与本地基线。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
        ],
        "exit_signals": [
            "manifest 已写入目标范围、执行模式、来源资产与阶段状态。",
            "evidence registry 已记录可追溯证据入口。",
        ],
        "lint_focus": [
            "manifest 必填字段",
            "source asset 路径存在性",
            "evidence location 可追溯性",
        ],
    },
    "architecture_convergence": {
        "purpose": "把旧资产、外部借鉴与本地约束收敛成单技能多阶段目标形态。",
        "entry_requirements": [
            "research_baseline 已形成可用 manifest 与 evidence registry。",
            "已识别需要保留、推翻与升级的旧结论。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["evidence_registry"],
            WORKSPACE_LAYOUT["architecture_decisions"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["architecture_decisions"],
        ],
        "exit_signals": [
            "architecture decisions 已引用旧资产与证据。",
            "目标形态与阶段门禁已经显式建模。",
        ],
        "lint_focus": [
            "decision 引用有效性",
            "target_shape 与 phase_gate 完整性",
            "前置 research_baseline 状态一致性",
        ],
    },
    "plan": {
        "purpose": "把目标形态拆成最小切片施工合同。",
        "entry_requirements": [
            "architecture_convergence 已形成有效 decision。",
            "当前目标形态可映射成离散施工切片。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["architecture_decisions"],
            WORKSPACE_LAYOUT["plan_slices"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["plan_slices"],
        ],
        "exit_signals": [
            "至少存在 1 个可施工切片。",
            "active slice 唯一。",
            "每个 active slice 都定义了验证方法、写回目标与退出信号。",
        ],
        "lint_focus": [
            "slice 字段完整性",
            "borrowed_design_refs 有效性",
            "active slice 唯一性",
        ],
    },
    "implementation": {
        "purpose": "围绕 active slice 做真实施工、验证与逐回合证据写回。",
        "entry_requirements": [
            "plan 已存在 active slice。",
            "active slice 已写明验证方法、证据要求与写回目标。",
        ],
        "required_objects": [
            WORKSPACE_LAYOUT["manifest"],
            WORKSPACE_LAYOUT["plan_slices"],
            WORKSPACE_LAYOUT["implementation_ledger"],
        ],
        "writeback_targets": [
            WORKSPACE_LAYOUT["implementation_ledger"],
            WORKSPACE_LAYOUT["manifest"],
        ],
        "exit_signals": [
            "当回合实现、验证、状态裁决与残余问题已写入 ledger。",
            "完成切片时可从 ledger 回溯到验证与证据。",
        ],
        "lint_focus": [
            "ledger -> slice 引用关系",
            "validation_runs 与 evidence_refs 完整性",
            "状态更新与切片完成信号一致性",
        ],
    },
    "validation": {
        "purpose": "对对象层、阶段沉淀文档层与写回状态做最终一致性收口。",
        "entry_requirements": [
            "对象层已经具备最小闭环。",
            "需要验证阶段沉淀文档、方案文档与状态位是否一致。",
        ],
        "required_objects": list(WORKSPACE_LAYOUT.values()),
        "writeback_targets": [
            WORKSPACE_LAYOUT["manifest"],
        ],
        "exit_signals": [
            "阶段状态、阶段文档与写回状态一致。",
            "不存在无证据结论、无写回实现与虚假完成阶段。",
        ],
        "lint_focus": [
            "跨阶段状态一致性",
            "阶段沉淀文档写回状态",
            "引用路径存在性",
        ],
    },
}


def runtime_contract_payload() -> dict[str, Any]:
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
            "workspace-scaffold",
        ],
        "stage_order": STAGE_ORDER,
        "workspace_layout": WORKSPACE_LAYOUT,
        "layout_rule": "文档链与阶段顺序保持一致；小型对象是真相源，阶段沉淀文档是汇总层。",
        "compiler_rule": "SKILL.md 只暴露 analysis_loop 入口；下游 markdown 通过 reading_chain 编译完整上下文。",
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
    return {"stage": stage, **STAGES[stage], "workspace_layout": WORKSPACE_LAYOUT}


def scaffold_workspace(workspace_root: Path, force: bool = False) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    manifest = {
        "analysis_id": "fill_me",
        "intent_summary": "fill_me",
        "execution_mode": "continuous",
        "single_stage_focus": None,
        "current_stage": "research_baseline",
        "source_assets": [],
        "target_scope": {"external_target": "", "local_target": ""},
        "stage_status": {
            "research_baseline": "in_progress",
            "architecture_convergence": "pending",
            "plan": "pending",
            "implementation": "pending",
            "validation": "pending",
        },
        "writeback_status": {
            "analysis_summary": "",
            "convergence_plan": "",
            "last_synced_at": "",
            "notes": "",
        },
    }
    files = {
        WORKSPACE_LAYOUT["manifest"]: manifest,
        WORKSPACE_LAYOUT["evidence_registry"]: {"evidence_items": []},
        WORKSPACE_LAYOUT["architecture_decisions"]: {"decisions": []},
        WORKSPACE_LAYOUT["plan_slices"]: {"slices": []},
        WORKSPACE_LAYOUT["implementation_ledger"]: {"entries": []},
    }
    created: list[str] = []
    skipped: list[str] = []
    for relative, payload in files.items():
        target = workspace_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            skipped.append(relative)
            continue
        target.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
        created.append(relative)
    return {
        "status": "ok",
        "workspace_root": str(workspace_root),
        "created_files": created,
        "skipped_files": skipped,
        "workspace_layout": WORKSPACE_LAYOUT,
    }


def stage_lint_payload(workspace_root: Path, stage: str) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
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
            "checked_files": {key: str((workspace_root / value).resolve()) for key, value in WORKSPACE_LAYOUT.items()},
        }

    manifest = loaded["manifest"]
    source_asset_ids = _validate_manifest(workspace_root, manifest, errors, warnings)
    evidence_ids = _validate_evidence_registry(workspace_root, loaded["evidence_registry"], errors, warnings)

    if stage in {"architecture_convergence", "plan", "implementation", "validation", "all"}:
        decision_ids = _validate_architecture_decisions(
            loaded["architecture_decisions"],
            source_asset_ids,
            evidence_ids,
            errors,
        )
    else:
        decision_ids = set()

    if stage in {"plan", "implementation", "validation", "all"}:
        slice_ids, active_slice_ids, completed_slice_ids = _validate_plan_slices(
            loaded["plan_slices"],
            decision_ids,
            errors,
        )
    else:
        slice_ids, active_slice_ids, completed_slice_ids = set(), [], []

    if stage in {"implementation", "validation", "all"}:
        _validate_implementation_ledger(
            workspace_root,
            loaded["implementation_ledger"],
            slice_ids,
            evidence_ids,
            errors,
        )
        _validate_completed_slices_have_witness(
            loaded["implementation_ledger"],
            completed_slice_ids,
            errors,
        )

    _validate_stage_consistency(
        workspace_root,
        manifest,
        stage,
        active_slice_ids,
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
        "checked_files": {key: str((workspace_root / value).resolve()) for key, value in WORKSPACE_LAYOUT.items()},
    }


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
        "writeback_status",
    ]
    for key in required_keys:
        if key not in manifest:
            _error(errors, "missing_field", source, f"manifest 缺少字段：{key}")
    execution_mode = manifest.get("execution_mode")
    if execution_mode not in {"continuous", "single_stage"}:
        _error(errors, "invalid_execution_mode", source, "execution_mode 只能是 continuous 或 single_stage。")
    current_stage = manifest.get("current_stage")
    if current_stage not in STAGE_ORDER:
        _error(errors, "invalid_current_stage", source, "current_stage 不在固定阶段列表内。")
    if execution_mode == "single_stage":
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
    source_assets = manifest.get("source_assets")
    if not isinstance(source_assets, list):
        _error(errors, "invalid_source_assets", source, "source_assets 必须是列表。")
        source_assets = []
    for index, asset in enumerate(source_assets):
        asset_source = f"{source}:source_assets[{index}]"
        if not isinstance(asset, dict):
            _error(errors, "invalid_asset_item", asset_source, "source asset 必须是映射。")
            continue
        asset_id = asset.get("asset_id")
        asset_path = asset.get("path")
        role = asset.get("role")
        if not isinstance(asset_id, str) or not asset_id:
            _error(errors, "missing_asset_id", asset_source, "source asset 缺少 asset_id。")
        elif asset_id in source_asset_ids:
            _error(errors, "duplicate_asset_id", asset_source, f"重复的 asset_id：{asset_id}")
        else:
            source_asset_ids.add(asset_id)
        if not isinstance(role, str) or not role:
            _error(errors, "missing_asset_role", asset_source, "source asset 缺少 role。")
        if not isinstance(asset_path, str) or not asset_path:
            _error(errors, "missing_asset_path", asset_source, "source asset 缺少 path。")
        else:
            resolved = _resolve_local_path(asset_path, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_asset_path_target", asset_source, f"source asset 路径不存在：{resolved}")
    if not source_assets:
        _warning(warnings, "empty_source_assets", source, "source_assets 为空；research_baseline 未完成。")
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
        _warning(warnings, "empty_evidence_registry", source, "evidence registry 为空；research_baseline 未完成。")
    return evidence_ids


def _validate_architecture_decisions(
    decisions_payload: dict[str, Any],
    source_asset_ids: set[str],
    evidence_ids: set[str],
    errors: list[dict[str, str]],
) -> set[str]:
    source = WORKSPACE_LAYOUT["architecture_decisions"]
    decisions = decisions_payload.get("decisions")
    decision_ids: set[str] = set()
    if not isinstance(decisions, list):
        _error(errors, "invalid_decisions", source, "decisions 必须是列表。")
        return decision_ids
    for index, decision in enumerate(decisions):
        item_source = f"{source}:decisions[{index}]"
        if not isinstance(decision, dict):
            _error(errors, "invalid_decision_item", item_source, "decision 必须是映射。")
            continue
        decision_id = decision.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id:
            _error(errors, "missing_decision_id", item_source, "decision 缺少 decision_id。")
        elif decision_id in decision_ids:
            _error(errors, "duplicate_decision_id", item_source, f"重复的 decision_id：{decision_id}")
        else:
            decision_ids.add(decision_id)
        for field in ("inherited_asset_refs", "evidence_refs", "current_baseline_delta", "target_shape", "phase_gate", "status"):
            if field not in decision:
                _error(errors, "missing_decision_field", item_source, f"decision 缺少字段：{field}")
        for ref in decision.get("inherited_asset_refs", []):
            if ref not in source_asset_ids:
                _error(errors, "invalid_inherited_asset_ref", item_source, f"未找到 source asset ref：{ref}")
        for ref in decision.get("evidence_refs", []):
            if ref not in evidence_ids:
                _error(errors, "invalid_decision_evidence_ref", item_source, f"未找到 evidence ref：{ref}")
        phase_gate = decision.get("phase_gate")
        if not isinstance(phase_gate, dict):
            _error(errors, "invalid_phase_gate", item_source, "phase_gate 必须是映射。")
        else:
            entry_requirements = phase_gate.get("entry_requirements")
            exit_signal = phase_gate.get("exit_signal")
            if not isinstance(entry_requirements, list):
                _error(errors, "invalid_phase_gate_entry", item_source, "phase_gate.entry_requirements 必须是列表。")
            if not isinstance(exit_signal, str) or not exit_signal:
                _error(errors, "missing_phase_gate_exit", item_source, "phase_gate.exit_signal 不能为空。")
        if decision.get("status") not in STAGE_STATUS_VALUES:
            _error(errors, "invalid_decision_status", item_source, "decision.status 必须使用阶段状态值。")
    return decision_ids


def _validate_plan_slices(
    slices_payload: dict[str, Any],
    decision_ids: set[str],
    errors: list[dict[str, str]],
) -> tuple[set[str], list[str], list[str]]:
    source = WORKSPACE_LAYOUT["plan_slices"]
    slices = slices_payload.get("slices")
    slice_ids: set[str] = set()
    active_slice_ids: list[str] = []
    completed_slice_ids: list[str] = []
    if not isinstance(slices, list):
        _error(errors, "invalid_slices", source, "slices 必须是列表。")
        return slice_ids, active_slice_ids, completed_slice_ids
    for index, slice_item in enumerate(slices):
        item_source = f"{source}:slices[{index}]"
        if not isinstance(slice_item, dict):
            _error(errors, "invalid_slice_item", item_source, "slice 必须是映射。")
            continue
        slice_id = slice_item.get("slice_id")
        if not isinstance(slice_id, str) or not slice_id:
            _error(errors, "missing_slice_id", item_source, "slice 缺少 slice_id。")
        elif slice_id in slice_ids:
            _error(errors, "duplicate_slice_id", item_source, f"重复的 slice_id：{slice_id}")
        else:
            slice_ids.add(slice_id)
        for field in (
            "borrowed_design_refs",
            "current_baseline_delta",
            "expected_effect",
            "validation_method",
            "required_evidence",
            "writeback_targets",
            "exit_signal",
            "status",
        ):
            if field not in slice_item:
                _error(errors, "missing_slice_field", item_source, f"slice 缺少字段：{field}")
        for ref in slice_item.get("borrowed_design_refs", []):
            if ref not in decision_ids:
                _error(errors, "invalid_borrowed_design_ref", item_source, f"未找到 borrowed_design_ref：{ref}")
        status = slice_item.get("status")
        if status not in SLICE_STATUS_VALUES:
            _error(errors, "invalid_slice_status", item_source, f"slice.status 必须属于 {sorted(SLICE_STATUS_VALUES)}。")
        elif status == "active" and isinstance(slice_id, str) and slice_id:
            active_slice_ids.append(slice_id)
        elif status == "completed" and isinstance(slice_id, str) and slice_id:
            completed_slice_ids.append(slice_id)
    if len(active_slice_ids) > 1:
        _error(errors, "multiple_active_slices", source, "同一时刻只能存在 1 个 active slice。")
    return slice_ids, active_slice_ids, completed_slice_ids


def _validate_implementation_ledger(
    workspace_root: Path,
    ledger_payload: dict[str, Any],
    slice_ids: set[str],
    evidence_ids: set[str],
    errors: list[dict[str, str]],
) -> None:
    source = WORKSPACE_LAYOUT["implementation_ledger"]
    entries = ledger_payload.get("entries")
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
        slice_id = entry.get("slice_id")
        if not isinstance(slice_id, str) or slice_id not in slice_ids:
            _error(errors, "invalid_entry_slice_id", item_source, f"ledger entry 必须引用有效 slice_id：{slice_id}")
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


def _validate_completed_slices_have_witness(
    ledger_payload: dict[str, Any],
    completed_slice_ids: list[str],
    errors: list[dict[str, str]],
) -> None:
    if not completed_slice_ids:
        return
    entries = ledger_payload.get("entries", [])
    for slice_id in completed_slice_ids:
        has_witness = False
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            if entry.get("slice_id") != slice_id:
                continue
            if entry.get("validation_runs") and entry.get("evidence_refs"):
                has_witness = True
                break
        if not has_witness:
            _error(
                errors,
                "completed_slice_without_witness",
                WORKSPACE_LAYOUT["implementation_ledger"],
                f"已完成切片 {slice_id} 没有对应验证与证据记录。",
            )


def _validate_stage_consistency(
    workspace_root: Path,
    manifest: dict[str, Any],
    requested_stage: str,
    active_slice_ids: list[str],
    ledger_payload: dict[str, Any],
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
) -> None:
    source = WORKSPACE_LAYOUT["manifest"]
    stage_status = manifest.get("stage_status", {})
    execution_mode = manifest.get("execution_mode")
    current_stage = manifest.get("current_stage")
    if execution_mode == "continuous" and current_stage in STAGE_ORDER:
        current_index = STAGE_ORDER.index(current_stage)
        for index, stage in enumerate(STAGE_ORDER):
            value = stage_status.get(stage)
            if index < current_index and value != "completed":
                _error(errors, "incomplete_previous_stage", source, f"连续执行模式下，前置阶段 {stage} 必须是 completed。")
    if requested_stage in {"plan", "implementation", "validation", "all"}:
        if stage_status.get("plan") in {"in_progress", "completed"} and len(active_slice_ids) > 1:
            _error(errors, "invalid_active_slice_count", source, "plan/implementation 阶段不允许多个 active slice。")
    if requested_stage in {"implementation", "validation", "all"}:
        implementation_status = stage_status.get("implementation")
        entries = ledger_payload.get("entries", [])
        if implementation_status in {"in_progress", "completed"} and not entries:
            _error(errors, "implementation_without_ledger", source, "implementation 已启动，但 ledger 为空。")
        if implementation_status == "in_progress" and not active_slice_ids:
            _error(errors, "implementation_without_active_slice", source, "implementation 进行中时必须存在 active slice。")
    if requested_stage in {"validation", "all"}:
        writeback = manifest.get("writeback_status", {})
        for field in ("analysis_summary", "convergence_plan"):
            target = writeback.get(field)
            if not isinstance(target, str) or not target:
                _error(errors, "missing_writeback_target", source, f"validation 阶段要求声明 {field} 写回路径。")
                continue
            resolved = _resolve_local_path(target, workspace_root)
            if resolved is not None and not resolved.exists():
                _error(errors, "missing_writeback_path", source, f"{field} 路径不存在：{resolved}")
        if stage_status.get("validation") == "completed":
            for stage in STAGE_ORDER:
                if stage_status.get(stage) != "completed":
                    _error(errors, "validation_completed_but_stage_open", source, f"validation 已完成，但 {stage} 不是 completed。")
    if stage_status.get("validation") == "pending" and requested_stage == "validation":
        _warning(warnings, "validation_not_started", source, "当前在 validation 阶段执行 lint，但 manifest 仍标记为 pending。")


def _resolve_local_path(raw_path: str, workspace_root: Path) -> Path | None:
    if raw_path.startswith(REMOTE_PREFIXES):
        return None
    path = Path(raw_path)
    if not path.is_absolute():
        path = workspace_root / path
    return path.resolve()


def _error(errors: list[dict[str, str]], code: str, source: str, message: str) -> None:
    errors.append({"code": code, "source": source, "message": message})


def _warning(warnings: list[dict[str, str]], code: str, source: str, message: str) -> None:
    warnings.append({"code": code, "source": source, "message": message})
