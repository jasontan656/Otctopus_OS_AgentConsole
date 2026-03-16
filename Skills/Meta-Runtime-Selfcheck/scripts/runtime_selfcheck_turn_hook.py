from __future__ import annotations

import json
import time
from pathlib import Path

from runtime_pain_batch_kernel import _group_items
from runtime_pain_observability import normalize_text
from runtime_pain_repair_exec import execute_command_list
from runtime_pain_types import AutoRepairRecord
from runtime_pain_types import CommandExecutionResult
from runtime_pain_types import TurnEvidence
from runtime_pain_types import TurnGroupSummary
from runtime_pain_types import TurnHookAudit
from runtime_pain_types import TurnHookResult
from runtime_pain_types import WatchSessionsResult
from runtime_selfcheck_session_source import build_session_fallback_queue
from runtime_selfcheck_session_source import collect_turn_evidence
from runtime_selfcheck_session_source import find_session_files
from runtime_selfcheck_session_source import resolve_codex_home
from runtime_selfcheck_session_source import _session_id_from_path
from runtime_selfcheck_store import ensure_store_exists
from runtime_selfcheck_store import iso_now
from runtime_selfcheck_store import load_watcher_state
from runtime_selfcheck_store import save_turn_audit
from runtime_selfcheck_store import save_watcher_state
from runtime_selfcheck_store import turn_audit_json_path
from runtime_selfcheck_store import watcher_state_json_path


def _latest_turn(turns: list[TurnEvidence]) -> TurnEvidence:
    ordered = sorted(
        turns,
        key=lambda row: (
            str(row.get("completed_at", "") or row.get("started_at", "") or ""),
            str(row.get("turn_id", "") or ""),
        ),
        reverse=True,
    )
    return ordered[0] if ordered else {}


def _candidate_auto_repairs(items: list[dict[str, object]], *, limit: int) -> list[AutoRepairRecord]:
    repairs: list[AutoRepairRecord] = []
    seen_commands: set[str] = set()
    for item in items:
        auto = item.get("auto_repair", {}) if isinstance(item.get("auto_repair", {}), dict) else {}
        command = str(auto.get("command", "") or "").strip()
        if not command or command in seen_commands:
            continue
        repairs.append(
            {
                "optimization_id": str(item.get("optimization_id", "") or ""),
                "repair_type": str(auto.get("repair_type", "") or ""),
                "command": command,
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


def run_turn_hook(
    *,
    codex_home_override: str | None = None,
    session_id: str | None = None,
    turn_id: str | None = None,
    mode: str = "diagnose",
    auto_repair: bool = False,
    auto_repair_limit: int = 3,
) -> TurnHookResult:
    ensure_store_exists()
    effective_auto_repair = auto_repair or mode == "repair"
    turns = collect_turn_evidence(
        codex_home_override=codex_home_override,
        session_id_filter=session_id,
        turn_id_filter=turn_id,
    )
    turn = _latest_turn(turns)
    if not turn:
        return {
            "status": "ok",
            "hook_mode": mode,
            "turn_hook_status": "no_turn_detected",
            "issues_detected": 0,
        }

    queue = build_session_fallback_queue(
        codex_home_override=codex_home_override,
        session_id_filter=str(turn.get("session_id", "") or ""),
        turn_id_filter=str(turn.get("turn_id", "") or ""),
        include_resolved=True,
        max_results=200,
    )
    items = queue.get("items", []) if isinstance(queue.get("items", []), list) else []
    grouped = _group_items(items)
    repairs = _candidate_auto_repairs(items, limit=auto_repair_limit) if effective_auto_repair else []
    execution_result: CommandExecutionResult = {
        "total_commands": 0,
        "success_commands": 0,
        "failed_commands": 0,
        "all_succeeded": False,
        "runs": [],
    }
    resolved_ids: list[str] = []
    if repairs:
        execution_result = execute_command_list(
            commands=[row["command"] for row in repairs],
            timeout_sec=20,
            workdir=str(turn.get("cwd", "") or ""),
            change_detection_root=str(turn.get("cwd", "") or ""),
        )
        resolved_ids = _resolved_ids_from_repairs(repairs=repairs, execution_result=execution_result)
        for item in items:
            if str(item.get("optimization_id", "") or "") in resolved_ids:
                item["is_resolved"] = True
        grouped = _group_items(items)

    pending_items = sum(1 for item in items if not bool(item.get("is_resolved", False)))
    audit_payload: TurnHookAudit = {
        "session_id": str(turn.get("session_id", "") or ""),
        "turn_id": str(turn.get("turn_id", "") or ""),
        "session_file": str(turn.get("session_file", "") or ""),
        "started_at": str(turn.get("started_at", "") or ""),
        "completed_at": str(turn.get("completed_at", "") or ""),
        "hook_mode": mode,
        "hook_status": "repaired" if resolved_ids else ("issues_detected" if items else "smooth"),
        "source_mode": "session_fallback",
        "cwd": str(turn.get("cwd", "") or ""),
        "user_message": str(turn.get("user_message", "") or ""),
        "issues_detected": len(items),
        "pending_issues": pending_items,
        "resolved_optimization_ids": resolved_ids,
        "group_count": int(grouped.get("group_count", 0) or 0),
        "groups": grouped.get("groups", []),
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
