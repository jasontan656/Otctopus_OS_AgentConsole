from __future__ import annotations

from typing import Any

from runtime_pain_types import FocusGroupSummary, RuntimePainGroup


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _first_dict(values: list[Any]) -> dict[str, Any]:
    return next((row for row in values if isinstance(row, dict)), {})


def _first_text(values: list[Any]) -> str:
    return next((str(row) for row in values if str(row).strip()), "")


def build_focus_group(groups: list[RuntimePainGroup]) -> FocusGroupSummary:
    if not groups:
        return {}
    focus = _as_dict(groups[0])
    diagnosis_card = _as_dict(focus.get("diagnosis_card_v2", {}))
    evidence_samples = _as_list(diagnosis_card.get("fact_evidence_samples", []))
    action_plan = _as_list(diagnosis_card.get("action_plan_v1", []))
    acceptance_checks = _as_list(diagnosis_card.get("acceptance_checks_v1", []))
    repair_strategy = _as_dict(diagnosis_card.get("repair_strategy_v2", {}))
    how_to_fix = _as_list(repair_strategy.get("how_to_fix_v1", []))
    adjudicated_directives = _as_list(repair_strategy.get("adjudicated_directives_v1", []))
    target_state = _as_list(repair_strategy.get("target_state_v1", []))
    expected_results = _as_list(repair_strategy.get("expected_results_v1", []))
    verification_runbook = _as_list(repair_strategy.get("verification_runbook_v1", []))
    routing_table = _as_list(repair_strategy.get("routing_table_v1", []))
    resolve_guard = _as_dict(repair_strategy.get("resolve_guard_v1", {}))
    first_directive = _first_dict(adjudicated_directives)
    first_route = _first_dict(routing_table)
    first_fix = _first_dict(how_to_fix)
    first_verification = _first_dict(verification_runbook)
    manager_story = _as_dict(diagnosis_card.get("manager_story_v1", {}))
    meta_reasoningchain = _as_dict(diagnosis_card.get("meta_reasoningchain_v1", {}))
    future_shape = _as_dict(meta_reasoningchain.get("future_shape", {}))
    before_state = _as_dict(future_shape.get("before_state_v1", {}))
    after_state_target = _as_dict(future_shape.get("after_state_target_v1", {}))
    change_manifest = _as_dict(future_shape.get("change_manifest_v1", {}))
    decision_recommendation = _as_dict(meta_reasoningchain.get("decision_recommendation", {}))

    first_action = _first_dict(action_plan)
    immediate_next_step = _first_text(_as_list(first_action.get("steps", [])))

    how_to_fix_now_parts: list[str] = []
    primary_decision = str(first_directive.get("decision", "") or "")
    fallback_instruction = str(first_fix.get("how_to_implement", "") or "")
    if primary_decision:
        how_to_fix_now_parts.append(primary_decision)
    if fallback_instruction and fallback_instruction != primary_decision:
        how_to_fix_now_parts.append(fallback_instruction)

    return {
        "pain_group_key": str(focus.get("pain_group_key", "") or ""),
        "pain_topic": str(focus.get("pain_topic", "") or ""),
        "priority_top": str(focus.get("priority_top", "") or ""),
        "pending_items": int(focus.get("pending_items", 0) or 0),
        "selection_reason": "按 pending_items/priority/latest_updated_at 排序后优先项。",
        "problem_statement": str(focus.get("problem_statement", "") or ""),
        "first_evidence": evidence_samples[0] if evidence_samples else {},
        "immediate_next_step": immediate_next_step,
        "what_we_were_doing": str(manager_story.get("what_we_were_doing", "") or ""),
        "expected_result": str(manager_story.get("expected_result", "") or ""),
        "actual_result": str(manager_story.get("actual_result", "") or ""),
        "why_this_created_hesitation": str(manager_story.get("why_this_created_hesitation", "") or ""),
        "strengthening_plan": str(manager_story.get("strengthening_plan", "") or ""),
        "executive_summary": str(manager_story.get("executive_summary", "") or ""),
        "decision_state": str(repair_strategy.get("decision_state", "") or ""),
        "how_to_fix_now": "；".join(how_to_fix_now_parts),
        "adjudicated_directive_now": first_directive,
        "route_now": first_route,
        "routing_table_preview": routing_table[:4],
        "resolve_guard_summary": {
            "guard_state": str(resolve_guard.get("guard_state", "") or ""),
            "repair_mode_behavior": str(resolve_guard.get("repair_mode_behavior", "") or ""),
            "deny_result_state": str(resolve_guard.get("deny_result_state", "") or ""),
        },
        "before_state_v1": before_state,
        "after_state_target_v1": after_state_target,
        "change_manifest_v1": change_manifest,
        "reasoning_decision_recommendation": decision_recommendation,
        "meta_reasoningchain_v1": meta_reasoningchain,
        "target_state_after_fix": _first_text(target_state),
        "expected_result_after_fix": _first_text(expected_results),
        "verification_next_check": "；".join(
            row
            for row in [
                str(first_verification.get("check", "") or ""),
                str(first_verification.get("expected_signal", "") or ""),
            ]
            if row
        ),
        "acceptance_preview": [str(row) for row in acceptance_checks[:3]],
    }
