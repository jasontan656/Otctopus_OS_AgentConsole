from __future__ import annotations

import json
import time
from pathlib import Path

from runtime_pain_batch_kernel import _group_items
from runtime_pain_observability import normalize_text
from runtime_pain_repair_exec import execute_command_list
from runtime_pain_types import AutoRepairRecord
from runtime_pain_types import CommandExecutionResult
from runtime_pain_types import TurnGroupSummary
from runtime_pain_types import TurnHookAudit
from runtime_pain_types import TurnHookResult
from runtime_pain_types import WatchSessionsResult
from runtime_selfcheck_command_governance import load_expected_failure_rules
from runtime_selfcheck_optimization_audit import build_turn_optimization_audit
from runtime_selfcheck_session_source import build_session_fallback_queue
from runtime_selfcheck_session_source import find_session_files
from runtime_selfcheck_session_source import load_target_turn_evidence
from runtime_selfcheck_session_source import resolve_codex_home
from runtime_selfcheck_session_source import _session_id_from_path
from runtime_selfcheck_store import ensure_store_exists
from runtime_selfcheck_store import iso_now
from runtime_selfcheck_store import load_watcher_state
from runtime_selfcheck_store import save_turn_audit
from runtime_selfcheck_store import save_watcher_state
from runtime_selfcheck_store import turn_audit_json_path
from runtime_selfcheck_store import watcher_state_json_path


def _candidate_auto_repairs(items: list[dict[str, object]], *, limit: int) -> list[AutoRepairRecord]:
    repairs: list[AutoRepairRecord] = []
    seen_commands: set[str] = set()
    for item in items:
        auto = item.get("auto_repair", {}) if isinstance(item.get("auto_repair", {}), dict) else {}
        decision = str(auto.get("decision", "") or "")
        if decision and decision != "immediate_repair":
            continue
        command = str(auto.get("command", "") or "").strip()
        if not command or command in seen_commands:
            continue
        repairs.append(
            {
                "optimization_id": str(item.get("optimization_id", "") or ""),
                "repair_type": str(auto.get("repair_type", "") or ""),
                "command": command,
                "workdir": str(auto.get("workdir", "") or ""),
                "change_detection_root": str(auto.get("change_detection_root", "") or ""),
                "decision": decision,
                "keyword_first_decision": str(auto.get("keyword_first_decision", "") or ""),
            }
        )
        seen_commands.add(command)
        if len(repairs) >= max(1, int(limit)):
            break
    return repairs


def _resolved_ids_from_repairs(
    *,
    repairs: list[AutoRepairRecord],
    execution_result: CommandExecutionResult,
) -> list[str]:
    runs = execution_result.get("runs", []) if isinstance(execution_result.get("runs", []), list) else []
    resolved: list[str] = []
    for repair, run in zip(repairs, runs):
        if not isinstance(run, dict):
            continue
        if str(run.get("status", "") or "") == "ok":
            resolved.append(str(repair.get("optimization_id", "") or ""))
    return resolved


def _empty_execution_result() -> CommandExecutionResult:
    return {
        "total_commands": 0,
        "success_commands": 0,
        "failed_commands": 0,
        "all_succeeded": False,
        "runs": [],
        "all_changed_paths": [],
        "all_changed_path_count": 0,
        "preflight_failed_commands": 0,
        "preflight_reason_codes": [],
        "change_detection_supported": False,
    }


def _merge_execution_results(results: list[CommandExecutionResult]) -> CommandExecutionResult:
    merged = _empty_execution_result()
    all_changed_paths: set[str] = set()
    preflight_reason_codes: list[str] = []
    runs: list[dict[str, object]] = []
    for result in results:
        merged["total_commands"] += int(result.get("total_commands", 0) or 0)
        merged["success_commands"] += int(result.get("success_commands", 0) or 0)
        merged["failed_commands"] += int(result.get("failed_commands", 0) or 0)
        merged["preflight_failed_commands"] += int(result.get("preflight_failed_commands", 0) or 0)
        preflight_reason_codes.extend(list(result.get("preflight_reason_codes", [])))
        runs.extend(list(result.get("runs", [])))
        all_changed_paths.update(str(path) for path in list(result.get("all_changed_paths", [])) if str(path).strip())
        merged["change_detection_supported"] = bool(merged.get("change_detection_supported", False) or result.get("change_detection_supported", False))
    merged["runs"] = runs
    merged["all_changed_paths"] = sorted(all_changed_paths)
    merged["all_changed_path_count"] = len(all_changed_paths)
    merged["preflight_reason_codes"] = sorted(set(preflight_reason_codes))
    merged["all_succeeded"] = bool(merged["total_commands"]) and int(merged["failed_commands"]) == 0
    return merged


def run_turn_hook(
    *,
    codex_home_override: str | None = None,
    session_id: str | None = None,
    turn_id: str | None = None,
    mode: str = "diagnose",
    auto_repair: bool = False,
    auto_repair_limit: int = 3,
    expected_failure_file: str | None = None,
    stage: str | None = None,
) -> TurnHookResult:
    ensure_store_exists()
    effective_auto_repair = auto_repair or mode == "repair"
    expected_failure_rules = load_expected_failure_rules(expected_failure_file)
    turn = load_target_turn_evidence(
        codex_home_override=codex_home_override,
        session_id_filter=session_id,
        turn_id_filter=turn_id,
    )
    if not turn:
        return {
            "status": "ok",
            "hook_mode": mode,
            "turn_hook_status": "no_turn_detected",
            "issues_detected": 0,
        }

    queue = build_session_fallback_queue(
        turns=[turn],
        turn_id_filter=str(turn.get("turn_id", "") or ""),
        include_resolved=True,
        max_results=200,
        expected_failure_rules=expected_failure_rules,
        stage=stage,
    )
    items = queue.get("items", []) if isinstance(queue.get("items", []), list) else []
    grouped = _group_items(items)
    optimization_audit = build_turn_optimization_audit(turn=turn, issue_items=items)
    repairs = _candidate_auto_repairs(items, limit=auto_repair_limit) if effective_auto_repair else []
    execution_result: CommandExecutionResult = _empty_execution_result()
    resolved_ids: list[str] = []
    if repairs:
        repair_runs: list[CommandExecutionResult] = []
        fallback_workdir = str(turn.get("cwd", "") or "")
        for repair in repairs:
            repair_runs.append(
                execute_command_list(
                    commands=[str(repair.get("command", "") or "")],
                    timeout_sec=20,
                    workdir=str(repair.get("workdir", "") or fallback_workdir),
                    change_detection_root=str(repair.get("change_detection_root", "") or fallback_workdir),
                )
            )
        execution_result = _merge_execution_results(repair_runs)
        resolved_ids = _resolved_ids_from_repairs(repairs=repairs, execution_result=execution_result)
        for item in items:
            if str(item.get("optimization_id", "") or "") in resolved_ids:
                item["is_resolved"] = True
        grouped = _group_items(items)

    issue_buckets = {
        "immediate_repair": 0,
        "strengthen_now": 0,
        "allow_expected_failure": 0,
        "pending_decision": 0,
    }
    keyword_first_buckets = {
        "rewrite": 0,
        "replace": 0,
        "add": 0,
    }
    strengthened_ids: list[str] = []
    expected_failure_ids: list[str] = []
    pending_decision_ids: list[str] = []
    confirmation_required_ids: list[str] = []
    for item in items:
        adjudication = str(item.get("adjudication", "") or "")
        if adjudication in issue_buckets:
            issue_buckets[adjudication] += 1
        keyword_first = item.get("keyword_first_edit", {}) if isinstance(item.get("keyword_first_edit", {}), dict) else {}
        keyword_decision = str(keyword_first.get("decision", "") or "")
        if keyword_decision in keyword_first_buckets:
            keyword_first_buckets[keyword_decision] += 1
        if adjudication == "strengthen_now":
            strengthened_ids.append(str(item.get("optimization_id", "") or ""))
        if adjudication == "allow_expected_failure":
            expected_failure_ids.append(str(item.get("optimization_id", "") or ""))
            item["is_resolved"] = True
        if adjudication == "pending_decision":
            pending_decision_ids.append(str(item.get("optimization_id", "") or ""))
        if bool(keyword_first.get("requires_user_confirmation", False)):
            confirmation_required_ids.append(str(item.get("optimization_id", "") or ""))
    pending_items = sum(1 for item in items if not bool(item.get("is_resolved", False)))
    audit_payload: TurnHookAudit = {
        "session_id": str(turn.get("session_id", "") or ""),
        "turn_id": str(turn.get("turn_id", "") or ""),
        "session_file": str(turn.get("session_file", "") or ""),
        "started_at": str(turn.get("started_at", "") or ""),
        "completed_at": str(turn.get("completed_at", "") or ""),
        "hook_mode": mode,
        "hook_status": (
            "repaired"
            if resolved_ids
            else (
                "issues_detected"
                if items
                else (
                    "optimization_opportunities_detected"
                    if int(optimization_audit.get("opportunity_count", 0) or 0) > 0
                    else "smooth"
                )
            )
        ),
        "source_mode": "session_fallback",
        "cwd": str(turn.get("cwd", "") or ""),
        "user_message": str(turn.get("user_message", "") or ""),
        "issues_detected": len(items),
        "pending_issues": pending_items,
        "resolved_optimization_ids": resolved_ids,
        "group_count": int(grouped.get("group_count", 0) or 0),
        "groups": grouped.get("groups", []),
        "issue_buckets": issue_buckets,
        "keyword_first_buckets": keyword_first_buckets,
        "optimization_audit_v1": optimization_audit,
        "expected_failure_ids": expected_failure_ids,
        "strengthened_optimization_ids": strengthened_ids,
        "pending_decision_ids": pending_decision_ids,
        "confirmation_required_ids": confirmation_required_ids,
        "auto_repairs": repairs,
        "repair_execution_v1": execution_result,
        "residual_risks": [
            normalize_text(str(item.get("summary", "") or ""), limit=220)
            for item in items
            if not bool(item.get("is_resolved", False))
        ][:8],
        "turn_audit_closeout": {
            "required": True,
            "ran_at": iso_now(),
            "status": "closed" if str(turn.get("status", "") or "") == "completed" else "open_turn_snapshot",
        },
    }
    saved = save_turn_audit(audit_payload)
    group_summary: TurnGroupSummary = {
        "group_count": int(grouped.get("group_count", 0) or 0),
        "pending_group_count": int(grouped.get("pending_group_count", 0) or 0),
        "resolved_group_count": int(grouped.get("resolved_group_count", 0) or 0),
    }
    return {
        "status": "ok",
        "hook_mode": mode,
        "turn_hook_status": str(saved.get("hook_status", "") or ""),
        "session_id": str(saved.get("session_id", "") or ""),
        "turn_id": str(saved.get("turn_id", "") or ""),
        "issues_detected": int(saved.get("issues_detected", 0) or 0),
        "pending_issues": int(saved.get("pending_issues", 0) or 0),
        "resolved_optimization_ids": list(saved.get("resolved_optimization_ids", [])),
        "turn_audit_path": str(turn_audit_json_path(str(saved.get("session_id", "") or ""), str(saved.get("turn_id", "") or ""))),
        "group_summary": group_summary,
        "source_mode": "session_fallback",
        "auto_repairs": repairs,
        "repair_execution_v1": execution_result,
        "issue_buckets": dict(saved.get("issue_buckets", {})),
        "keyword_first_buckets": dict(saved.get("keyword_first_buckets", {})),
        "confirmation_required_ids": list(saved.get("confirmation_required_ids", [])),
        "optimization_audit_v1": dict(saved.get("optimization_audit_v1", {})),
    }


def watch_codex_sessions(
    codex_home_override: str | None = None,
    *,
    poll_interval_ms: int = 500,
    idle_exit_seconds: float | None = None,
    once: bool = False,
    session_id_filter: str | None = None,
) -> WatchSessionsResult:
    ensure_store_exists()
    codex_home = resolve_codex_home(codex_home_override)
    watcher_state = load_watcher_state()
    file_cursors = {path: int(value or "0") for path, value in watcher_state.get("file_cursors", {}).items()}
    processed_turns: list[dict[str, Any]] = []
    processed_files = 0
    last_activity = time.monotonic()
    while True:
        activity_seen = False
        changed_session_ids: set[str] = set()
        for session_file in find_session_files(codex_home, session_id_filter=session_id_filter):
            cursor = file_cursors.get(str(session_file), 0)
            last_line = cursor
            with session_file.open("r", encoding="utf-8", errors="replace") as handle:
                for line_no, _ in enumerate(handle, start=1):
                    last_line = line_no
            if last_line <= cursor:
                continue
            file_cursors[str(session_file)] = last_line
            processed_files += 1
            activity_seen = True
            session_id = _session_id_from_path(session_file)
            if session_id:
                changed_session_ids.add(session_id)
        for session_id in sorted(changed_session_ids):
            payload = run_turn_hook(
                codex_home_override=str(codex_home),
                session_id=session_id,
                mode="diagnose",
                auto_repair=False,
            )
            if payload.get("turn_id"):
                processed_turns.append(payload)
        save_watcher_state(
            {
                "codex_home": str(codex_home),
                "updated_at": iso_now(),
                "file_cursors": {path: str(line_no) for path, line_no in sorted(file_cursors.items())},
            }
        )
        if once:
            break
        if activity_seen:
            last_activity = time.monotonic()
        elif idle_exit_seconds is not None and (time.monotonic() - last_activity) >= idle_exit_seconds:
            break
        time.sleep(max(100, int(poll_interval_ms)) / 1000.0)

    return {
        "status": "ok",
        "codex_home": str(codex_home),
        "processed_files": processed_files,
        "processed_turns": processed_turns,
        "watcher_state_json": str(watcher_state_json_path()),
    }
