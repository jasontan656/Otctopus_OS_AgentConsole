from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import (
    ACTION_TYPES,
    DESIGN_DECISION_MODES,
    PACKAGE_STATUS_VALUES,
    STAGE_ARTIFACTS,
    STAGE_ORDER,
    STAGE_REQUIRED_SECTIONS,
    STAGE_STATUS_VALUES,
    STAGE_UPSTREAM_REPORTS,
    WORKSPACE_LAYOUT,
)
from .validation_common import _error, _resolve_local_path, _warning


PLACEHOLDER_MARKERS = ("待补齐", "fill_me", "replace_me", "待当前任务在")


def _validate_non_empty_string(payload: dict[str, Any], field: str, source: str, errors: list[dict[str, str]]) -> None:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        _error(errors, "invalid_string_field", source, f"{field} 必须是非空字符串。")


def _validate_string_list(payload: dict[str, Any], field: str, source: str, errors: list[dict[str, str]], *, min_items: int = 1) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list):
        _error(errors, "invalid_list_field", source, f"{field} 必须是列表。")
        return []
    normalized: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            _error(errors, "invalid_list_item", f"{source}:{field}[{index}]", f"{field} 中只能包含非空字符串。")
            continue
        normalized.append(item)
    if len(normalized) < min_items:
        _error(errors, "empty_required_list", source, f"{field} 至少需要 {min_items} 条。")
    return normalized


def _validate_consumed_stage_reports(
    workspace_root: Path,
    payload: dict[str, Any],
    field: str,
    required_reports: list[str],
    source: str,
    errors: list[dict[str, str]],
) -> list[str]:
    consumed = _validate_string_list(payload, field, source, errors)
    consumed_set = set(consumed)
    missing = [report for report in required_reports if report not in consumed_set]
    if missing:
        _error(errors, "missing_consumed_stage_reports", source, f"{field} 缺少前序正式产物引用：{missing}")
    for index, report in enumerate(consumed):
        resolved = _resolve_local_path(report, workspace_root)
        if resolved is not None and not resolved.exists():
            _error(errors, "missing_consumed_stage_report_target", f"{source}:{field}[{index}]", f"前序正式产物路径不存在：{resolved}")
    return consumed


def _validate_evidence_refs(payload: dict[str, Any], field: str, evidence_ids: set[str], source: str, errors: list[dict[str, str]]) -> list[str]:
    refs = _validate_string_list(payload, field, source, errors)
    for index, ref in enumerate(refs):
        if ref not in evidence_ids:
            _error(errors, "invalid_evidence_ref", f"{source}:{field}[{index}]", f"未找到 evidence ref：{ref}")
    return refs


def _validate_stage_markdown(stage: str, target: Path, errors: list[dict[str, str]]) -> None:
    content = target.read_text(encoding="utf-8")
    source = STAGE_ARTIFACTS[stage]
    for marker in PLACEHOLDER_MARKERS:
        if marker in content:
            _error(errors, "placeholder_stage_report", source, f"{stage} 阶段产物仍包含占位文本：{marker}")
            break
    for section in STAGE_REQUIRED_SECTIONS[stage]:
        heading = f"## {section}"
        if heading not in content:
            _error(errors, "missing_stage_section", source, f"{stage} 阶段产物缺少章节：{heading}")
    for upstream in STAGE_UPSTREAM_REPORTS[stage]:
        if upstream not in content:
            _error(errors, "missing_upstream_report_reference", source, f"{stage} 阶段产物缺少前序正式产物引用：{upstream}")


def _validate_manifest(workspace_root: Path, manifest: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> set[str]:
    source = WORKSPACE_LAYOUT["manifest"]
    source_asset_ids: set[str] = set()
    required_keys = ["analysis_id", "intent_summary", "execution_mode", "current_stage", "source_assets", "target_scope", "stage_status", "stage_outputs", "writeback_status"]
    for key in required_keys:
        if key not in manifest:
            _error(errors, "missing_field", source, f"manifest 缺少字段：{key}")
    if manifest.get("execution_mode") not in {"continuous", "single_stage"}:
        _error(errors, "invalid_execution_mode", source, "execution_mode 只能是 continuous 或 single_stage。")
    if manifest.get("current_stage") not in STAGE_ORDER:
        _error(errors, "invalid_current_stage", source, "current_stage 不在固定阶段列表内。")
    if manifest.get("execution_mode") == "single_stage" and manifest.get("single_stage_focus") not in STAGE_ORDER:
        _error(errors, "invalid_single_stage_focus", source, "single_stage 模式必须声明有效的 single_stage_focus。")
    stage_status = manifest.get("stage_status")
    if not isinstance(stage_status, dict):
        _error(errors, "invalid_stage_status", source, "stage_status 必须是映射。")
        stage_status = {}
    for stage in STAGE_ORDER:
        if stage_status.get(stage) not in STAGE_STATUS_VALUES:
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


def _validate_evidence_registry(workspace_root: Path, evidence_registry: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> set[str]:
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


def _validate_architect_assessment(workspace_root: Path, payload: dict[str, Any], evidence_ids: set[str], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["architect_assessment"]
    _validate_consumed_stage_reports(workspace_root, payload, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["architect"], source, errors)
    _validate_string_list(payload, "question_framework", source, errors)
    _validate_string_list(payload, "judgement_chain", source, errors)
    _validate_string_list(payload, "should_change", source, errors)
    _validate_string_list(payload, "should_not_change", source, errors)
    _validate_string_list(payload, "open_questions", source, errors)
    _validate_non_empty_string(payload, "architecture_judgement", source, errors)
    _validate_evidence_refs(payload, "evidence_refs", evidence_ids, source, errors)


def _validate_preview_projection(workspace_root: Path, payload: dict[str, Any], evidence_ids: set[str], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["preview_projection"]
    _validate_consumed_stage_reports(workspace_root, payload, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["preview"], source, errors)
    _validate_string_list(payload, "question_framework", source, errors)
    _validate_string_list(payload, "reasoning_chain", source, errors)
    for field in ("future_shape", "behavior_delta", "failure_modes", "rollback_triggers"):
        _validate_string_list(payload, field, source, errors)
    _validate_evidence_refs(payload, "evidence_refs", evidence_ids, source, errors)


def _validate_design_decisions(workspace_root: Path, payload: dict[str, Any], evidence_ids: set[str], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["design_decisions"]
    _validate_consumed_stage_reports(workspace_root, payload, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["design"], source, errors)
    _validate_string_list(payload, "question_framework", source, errors)
    _validate_string_list(payload, "decision_chain", source, errors)
    if payload.get("decision_mode") not in DESIGN_DECISION_MODES:
        _error(errors, "invalid_decision_mode", source, f"decision_mode 必须属于 {sorted(DESIGN_DECISION_MODES)}。")
    _validate_non_empty_string(payload, "seamless_state", source, errors)
    _validate_evidence_refs(payload, "evidence_refs", evidence_ids, source, errors)
    decision_items = payload.get("decision_items")
    if not isinstance(decision_items, list):
        _error(errors, "invalid_decision_items", source, "decision_items 必须是列表。")
        return
    if not decision_items:
        _error(errors, "empty_decision_items", source, "decision_items 至少需要 1 条。")
    for index, item in enumerate(decision_items):
        item_source = f"{source}:decision_items[{index}]"
        if not isinstance(item, dict):
            _error(errors, "invalid_design_item", item_source, "decision item 必须是映射。")
            continue
        for field in ("title", "problem", "selected_because", "rationale"):
            if not isinstance(item.get(field), str) or not item.get(field):
                _error(errors, "missing_design_item_field", item_source, f"缺少字段：{field}")
        derives_from = item.get("derives_from_stage_reports")
        if not isinstance(derives_from, list) or not derives_from:
            _error(errors, "missing_design_item_reports", item_source, "derives_from_stage_reports 至少需要 1 条。")
        else:
            for sub_index, raw_path in enumerate(derives_from):
                if not isinstance(raw_path, str) or not raw_path:
                    _error(errors, "invalid_design_item_report", f"{item_source}:derives_from_stage_reports[{sub_index}]", "必须是非空字符串。")
                    continue
                resolved = _resolve_local_path(raw_path, workspace_root)
                if resolved is not None and not resolved.exists():
                    _error(errors, "missing_design_item_report_target", f"{item_source}:derives_from_stage_reports[{sub_index}]", f"前序正式产物路径不存在：{resolved}")
        if not isinstance(item.get("blocked_by"), list):
            _error(errors, "invalid_design_item_blocked_by", item_source, "blocked_by 必须是列表。")
        _validate_string_list(item, "rejected_options", item_source, errors)
        _validate_evidence_refs(item, "evidence_refs", evidence_ids, item_source, errors)


def _validate_impact_map(workspace_root: Path, payload: dict[str, Any], evidence_ids: set[str], errors: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["impact_map"]
    if payload.get("task_mode") not in {"READ_ONLY", "WRITE_INTENT"}:
        _error(errors, "invalid_task_mode", source, "task_mode 必须是 READ_ONLY 或 WRITE_INTENT。")
    _validate_consumed_stage_reports(workspace_root, payload, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["impact"], source, errors)
    _validate_string_list(payload, "question_framework", source, errors)
    _validate_string_list(payload, "judgement_chain", source, errors)
    for field in ("direct_scope", "indirect_scope", "latent_related", "validation_or_evidence", "must_update", "must_check_before_edit", "regression_surface"):
        _validate_string_list(payload, field, source, errors)
    _validate_evidence_refs(payload, "evidence_refs", evidence_ids, source, errors)
    _validate_non_empty_string(payload, "confidence", source, errors)
    evidence_gaps = payload.get("evidence_gaps")
    if not isinstance(evidence_gaps, list):
        _error(errors, "invalid_evidence_gaps", source, "evidence_gaps 必须是列表。")


def _validate_milestone_packages(workspace_root: Path, payload: dict[str, Any], errors: list[dict[str, str]]) -> tuple[set[str], list[str], list[str]]:
    source = WORKSPACE_LAYOUT["milestone_packages"]
    planning_basis = payload.get("planning_basis")
    if not isinstance(planning_basis, dict):
        _error(errors, "invalid_planning_basis", source, "planning_basis 必须是映射。")
        planning_basis = {}
    _validate_consumed_stage_reports(workspace_root, planning_basis, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["plan"], f"{source}:planning_basis", errors)
    _validate_string_list(planning_basis, "question_framework", f"{source}:planning_basis", errors)
    _validate_string_list(planning_basis, "package_derivation_chain", f"{source}:planning_basis", errors)
    packages = payload.get("milestone_packages")
    package_ids: set[str] = set()
    active_ids: list[str] = []
    completed_ids: list[str] = []
    if not isinstance(packages, list):
        _error(errors, "invalid_milestone_packages", source, "milestone_packages 必须是列表。")
        return package_ids, active_ids, completed_ids
    if not packages:
        _error(errors, "empty_milestone_packages", source, "milestone_packages 至少需要 1 个 package。")
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
        for field in ("goal", "consumes", "delivers", "validation", "status", "derives_from_stage_reports", "stage_gates", "writeback_targets", "evidence_expectations", "exit_signals"):
            if field not in item:
                _error(errors, "missing_package_field", item_source, f"package 缺少字段：{field}")
        if not isinstance(item.get("goal"), str) or not item.get("goal"):
            _error(errors, "invalid_package_goal", item_source, "goal 必须是非空字符串。")
        for field in ("consumes", "delivers", "validation", "derives_from_stage_reports", "stage_gates", "writeback_targets", "evidence_expectations", "exit_signals"):
            _validate_string_list(item, field, item_source, errors)
        blocked_by = item.get("blocked_by", [])
        if not isinstance(blocked_by, list):
            _error(errors, "invalid_package_blocked_by", item_source, "blocked_by 必须是列表。")
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


def _validate_implementation_ledger(workspace_root: Path, payload: dict[str, Any], package_ids: set[str], evidence_ids: set[str], errors: list[dict[str, str]]) -> None:
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
        for field in ("action_types", "summary", "changed_paths", "validation_runs", "evidence_refs", "status_updates", "residual_issues", "consumed_stage_reports", "preflight_checks", "derivation_notes", "writeback_targets"):
            if field not in entry:
                _error(errors, "missing_entry_field", item_source, f"ledger entry 缺少字段：{field}")
        _validate_consumed_stage_reports(workspace_root, entry, "consumed_stage_reports", STAGE_UPSTREAM_REPORTS["implementation"], item_source, errors)
        _validate_string_list(entry, "preflight_checks", item_source, errors)
        _validate_string_list(entry, "derivation_notes", item_source, errors)
        _validate_string_list(entry, "writeback_targets", item_source, errors)
        if not isinstance(entry.get("summary"), str) or not entry.get("summary"):
            _error(errors, "missing_entry_summary", item_source, "ledger entry 缺少 summary。")
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


def _validate_completed_packages_have_witness(payload: dict[str, Any], completed_package_ids: list[str], errors: list[dict[str, str]]) -> None:
    if not completed_package_ids:
        return
    entries = payload.get("entries", [])
    for package_id in completed_package_ids:
        has_witness = False
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("package_id") != package_id:
                continue
            if entry.get("validation_runs") and entry.get("evidence_refs"):
                has_witness = True
                break
        if not has_witness:
            _error(errors, "completed_package_without_witness", WORKSPACE_LAYOUT["implementation_ledger"], f"已完成 package {package_id} 没有对应验证与证据记录。")


def _validate_stage_artifacts(workspace_root: Path, manifest: dict[str, Any], requested_stage: str, errors: list[dict[str, str]]) -> None:
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
            continue
        if resolved is not None and resolved.suffix == ".md":
            _validate_stage_markdown(stage, resolved, errors)


def _validate_stage_consistency(workspace_root: Path, manifest: dict[str, Any], requested_stage: str, active_package_ids: list[str], ledger_payload: dict[str, Any], errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    source = WORKSPACE_LAYOUT["manifest"]
    stage_status = manifest.get("stage_status", {})
    current_stage = manifest.get("current_stage")
    execution_mode = manifest.get("execution_mode")
    if execution_mode == "continuous" and current_stage in STAGE_ORDER:
        current_index = STAGE_ORDER.index(current_stage)
        for index, stage in enumerate(STAGE_ORDER):
            if index < current_index and stage_status.get(stage) != "completed":
                _error(errors, "incomplete_previous_stage", source, f"连续执行模式下，前置阶段 {stage} 必须是 completed。")
    if requested_stage in {"plan", "implementation", "validation", "final_delivery", "all"} and stage_status.get("plan") in {"in_progress", "completed"} and len(active_package_ids) > 1:
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
