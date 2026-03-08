#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from runtime_pain_observability import attach_observability_logs, new_run_id
from runtime_pain_focus import build_focus_group
from runtime_pain_repair import (
    build_completion_message,
    compact_group,
    detect_preexisting_changes,
    execute_command_list,
    find_next_group,
    pending_groups,
    resolve_group_batch,
    select_current_group,
    select_current_groups,
)
from runtime_pain_batch_support import (
    DEFAULT_HISTORY,
    DEFAULT_MEMORY_RUNTIME,
    FORCED_SCOPE_MODE,
    HUMAN_LOG_NAME,
    HUMAN_RENDERER,
    HUMAN_SUMMARY_KEY,
    MACHINE_LOG_NAME,
    REPAIR_TOKEN,
    _build_report_only_output,
    _dedupe_ordered_items,
    _detect_mode,
    _group_items,
    _latest_session_id,
    _normalize_ordered_keys,
    _queue_items,
    _run_memory_runtime,
)

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Post-task runtime selfcheck: inspect previous-run pain points from an external provider, produce a remediation report, and only write back resolved status when explicitly asked."
    )
    ap.add_argument(
        "mode_token",
        nargs="*",
        help="Use `>` (or omit mode) to diagnose the previous run. Use `修复` only for explicit post-change writeback.",
    )
    ap.add_argument("--mode", default="auto", choices=["auto", "diagnose", "repair"])
    ap.add_argument(
        "--memory-runtime",
        default=DEFAULT_MEMORY_RUNTIME,
        help="Path to an external runtime pain provider implementing optimization-list and optional optimization-resolve.",
    )
    ap.add_argument("--history-path", default=str(DEFAULT_HISTORY))
    ap.add_argument("--session-id", default="")
    ap.add_argument("--thread-id", default=os.environ.get("CODEX_THREAD_ID", ""))
    ap.add_argument(
        "--session-scope-mode",
        default=FORCED_SCOPE_MODE,
        choices=["auto", "thread_scoped", "all_threads"],
        help="Accepted for compatibility, but runtime extraction is always enforced as all_threads.",
    )
    ap.add_argument("--max-results", type=int, default=200)
    ap.add_argument("--include-resolved", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--group-key", action="append", default=[])
    ap.add_argument("--resolved-by", default="2-Task-runtime-selfcheck")
    ap.add_argument("--turn-id", default="runtime-pain-batch")
    ap.add_argument("--dry-run", action=argparse.BooleanOptionalAction, default=False)
    ap.add_argument(
        "--repair-cmd",
        action="append",
        default=[],
        help="Deprecated: ignored. Code changes must be applied manually via apply_patch.",
    )
    ap.add_argument("--verify-cmd", action="append", default=[])
    ap.add_argument("--repair-timeout-sec", type=int, default=180)
    ap.add_argument("--repair-workdir", default="")
    ap.add_argument(
        "--auto-repair-cmd",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Deprecated: ignored. Runtime selfcheck no longer auto-executes repair commands.",
    )
    ap.add_argument("--manual-repair-applied", action=argparse.BooleanOptionalAction, default=False)
    ap.add_argument("--manual-repair-path", action="append", default=[])
    return ap


def _sum_execution_results(values: list[dict[str, Any]]) -> dict[str, Any]:
    if not values:
        return {
            "total_commands": 0,
            "success_commands": 0,
            "failed_commands": 0,
            "all_succeeded": False,
            "runs": [],
            "change_detection_supported": False,
            "all_changed_paths": [],
            "all_changed_path_count": 0,
            "preflight_failed_commands": 0,
            "preflight_reason_codes": [],
        }

    aggregated_runs: list[dict[str, Any]] = []
    total_commands = 0
    total_success = 0
    total_failed = 0
    preflight_failed = 0
    preflight_reasons: set[str] = set()
    has_detection = False
    changed_paths: set[str] = set()
    for row in values:
        if not isinstance(row, dict):
            continue
        total_commands += int(row.get("total_commands", 0) or 0)
        total_success += int(row.get("success_commands", 0) or 0)
        total_failed += int(row.get("failed_commands", 0) or 0)
        preflight_failed += int(row.get("preflight_failed_commands", 0) or 0)
        for reason_code in row.get("preflight_reason_codes", []) if isinstance(row.get("preflight_reason_codes", []), list) else []:
            normalized_reason = str(reason_code or "").strip()
            if normalized_reason:
                preflight_reasons.add(normalized_reason)
        has_detection = has_detection or bool(row.get("change_detection_supported", False))
        if row.get("all_changed_path_count", 0):
            paths = row.get("all_changed_paths", [])
            if isinstance(paths, list):
                changed_paths.update(str(x) for x in paths if str(x).strip())
        for run in row.get("runs", []) if isinstance(row.get("runs", []), list) else []:
            if isinstance(run, dict):
                aggregated_runs.append(run)

    return {
        "total_commands": total_commands,
        "success_commands": total_success,
        "failed_commands": total_failed,
        "all_succeeded": total_failed == 0 and total_commands > 0,
        "runs": aggregated_runs,
        "change_detection_supported": has_detection,
        "all_changed_paths": sorted(changed_paths),
        "all_changed_path_count": len(changed_paths),
        "preflight_failed_commands": preflight_failed,
        "preflight_reason_codes": sorted(preflight_reasons),
    }


def _normalize_manual_path_prefixes(values: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for raw in values:
        value = str(raw or "").strip()
        if not value:
            continue
        normalized = value.replace("\\", "/")
        if normalized.startswith("./"):
            normalized = normalized[2:]
        normalized = normalized.rstrip("/")
        if not normalized:
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def _strip_change_prefix(path_value: str) -> str:
    value = str(path_value or "").strip()
    if ":" in value:
        return value.split(":", 1)[1]
    return value


def _normalize_manual_prefix(prefix: str, repo_root: str) -> str:
    value = str(prefix or "").strip().replace("\\", "/").rstrip("/")
    if not value:
        return ""
    if value.startswith("./"):
        value = value[2:]

    root = str(repo_root or "").strip()
    if not root:
        return value
    try:
        root_path = Path(root).expanduser().resolve()
        value_path = Path(value).expanduser()
        if value_path.is_absolute():
            relative = value_path.resolve().relative_to(root_path)
            return str(relative).replace("\\", "/").rstrip("/")
    except Exception:
        return value
    return value


def _filter_changed_paths(paths: list[str], manual_path_prefixes: list[str], *, repo_root: str = "") -> list[str]:
    if not manual_path_prefixes:
        return [str(x) for x in paths if str(x).strip()]

    normalized_prefixes = [
        _normalize_manual_prefix(prefix, repo_root)
        for prefix in manual_path_prefixes
        if str(prefix or "").strip()
    ]

    filtered: list[str] = []
    seen: set[str] = set()
    for row in paths:
        text = str(row or "").strip()
        if not text:
            continue
        candidate = _strip_change_prefix(text).replace("\\", "/")
        if candidate.startswith("./"):
            candidate = candidate[2:]
        matched = False
        for normalized_prefix in normalized_prefixes:
            if candidate == normalized_prefix or candidate.startswith(f"{normalized_prefix}/"):
                matched = True
                break
        if not matched:
            continue
        if text in seen:
            continue
        seen.add(text)
        filtered.append(text)
    return filtered


def _emit_report_only_output(*, run_id: str, mode: str, output: dict[str, Any]) -> None:
    attach_observability_logs(run_id=run_id, mode=mode, output=output)
    report_only_output = _build_report_only_output(
        status=str(output.get("status", "ok") or "ok"),
        payload=output["runtime_pain_batch_selfcheck_v1"],
    )
    print(json.dumps(report_only_output, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()

    mode = _detect_mode(mode=args.mode, raw_tokens=list(args.mode_token or []))
    run_id = new_run_id(mode)
    memory_runtime_raw = str(args.memory_runtime or "").strip()
    if not memory_runtime_raw:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "pain_source_not_configured",
                    "hint": "Set CODEX_RUNTIME_PAIN_PROVIDER or pass --memory-runtime <provider.py>.",
                },
                ensure_ascii=False,
            )
        )
        return 1
    memory_runtime = Path(memory_runtime_raw).expanduser().resolve()
    if not memory_runtime.exists():
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "pain_source_not_found",
                    "pain_source": str(memory_runtime),
                },
                ensure_ascii=False,
            )
        )
        return 1

    queue = _queue_items(
        memory_runtime=memory_runtime,
        max_results=max(1, int(args.max_results)),
        include_resolved=bool(args.include_resolved),
        session_scope_mode=str(args.session_scope_mode or "auto"),
        thread_id=str(args.thread_id or "").strip(),
    )
    items = queue.get("items", []) if isinstance(queue, dict) else []
    if not isinstance(items, list):
        items = []

    grouped = _group_items(items)
    grouped_rows = grouped.get("groups", []) if isinstance(grouped.get("groups", []), list) else []
    requested_keys = _normalize_ordered_keys(args.group_key or [])
    selected_groups = select_current_groups(groups=grouped_rows, requested_keys=requested_keys)
    selected_group = selected_groups[0] if selected_groups else {}
    selected_group_key = str(selected_group.get("pain_group_key", "") or "")
    selected_group_keys = _normalize_ordered_keys(
        (str(g.get("pain_group_key", "") or "") for g in selected_groups)
    )
    selected_next_group = find_next_group(
        groups=grouped_rows,
        selected_group_keys=selected_group_keys,
    )
    selected_pending_groups = pending_groups(grouped_rows)
    all_resolved_before = len(selected_pending_groups) == 0
    output: dict[str, Any] = {
        "status": "ok",
        "runtime_pain_batch_selfcheck_v1": {
            "run_id": run_id,
            "mode": mode,
            "repair_token_required": REPAIR_TOKEN,
            "observability_contract": {
                "machine_log_name": MACHINE_LOG_NAME,
                "human_log_name": HUMAN_LOG_NAME,
                "human_renderer": HUMAN_RENDERER,
            },
            "scope_policy": "all_threads_enforced",
            "session_scope_mode": str(queue.get("session_scope_mode", "") or FORCED_SCOPE_MODE),
            "thread_id": str(queue.get("thread_id", "") or args.thread_id),
            "queue_summary": {
                "total_items": int(queue.get("total_items", 0) or 0),
                "pending_items": int(queue.get("pending_items", 0) or 0),
                "resolved_items": int(queue.get("resolved_items", 0) or 0),
            },
            "group_summary": {
                "group_count": int(grouped.get("group_count", 0) or 0),
                "pending_group_count": int(grouped.get("pending_group_count", 0) or 0),
                "resolved_group_count": int(grouped.get("resolved_group_count", 0) or 0),
            },
            HUMAN_SUMMARY_KEY: {
                "run_id": run_id,
                "mode": mode,
                "status": "ok",
                "human_log": HUMAN_LOG_NAME,
                "human_renderer": HUMAN_RENDERER,
                "summary": "Runtime pain batch selfcheck completed; use machine.jsonl and human.log for audits.",
            },
            "groups": grouped_rows,
            "focus_group_v2": build_focus_group(grouped_rows),
            "selection_policy_v1": {
                "mode": "multi-group-batch" if len(selected_group_keys) > 1 or "all" in requested_keys else "single-focus-first",
                "requested_group_keys": requested_keys,
                "selected_group_keys": selected_group_keys,
                "selected_group_key": selected_group_key,
            },
            "current_pain_v1": compact_group(selected_group),
            "next_pain_v1": compact_group(selected_next_group),
            "all_pain_resolved_v1": all_resolved_before,
            "completion_message_v1": build_completion_message(
                next_group=selected_next_group,
                all_resolved=all_resolved_before,
            ),
            "repair_writeback": {
                "enabled": mode == "repair",
                "requested_group_keys": [str(x) for x in (args.group_key or []) if str(x).strip()],
                "dry_run": bool(args.dry_run),
                "result": {"total_writes": 0, "success_writes": 0, "failed_writes": 0, "writes": []},
            },
            "repair_execution_v1": {
                "target_group_count": len(selected_group_keys),
                "selected_group_key": selected_group_key,
                "selected_group_keys": selected_group_keys,
                "repair_then_resolve_policy": True,
                "repair_commands": [],
                "verify_commands": [],
                "repair_result": {"total_commands": 0, "success_commands": 0, "failed_commands": 0, "all_succeeded": False, "runs": []},
                "verify_result": {"total_commands": 0, "success_commands": 0, "failed_commands": 0, "all_succeeded": False, "runs": []},
                "can_mark_resolved": False,
                "blocked_reason": "",
            },
        },
    }

    if mode != "repair":
        _emit_report_only_output(run_id=run_id, mode=mode, output=output)
        return 0

    groups = grouped_rows
    selected_groups = select_current_groups(groups=groups, requested_keys=requested_keys)
    selected_group = selected_groups[0] if selected_groups else {}
    selected_group_key = str(selected_group.get("pain_group_key", "") or "")
    verify_cmds_input = [str(x).strip() for x in (args.verify_cmd or []) if str(x).strip()]
    repair_workdir = str(args.repair_workdir or "").strip()
    manual_repair_applied = bool(args.manual_repair_applied)
    manual_path_prefixes = _normalize_manual_path_prefixes([str(x) for x in (args.manual_repair_path or [])])

    repair_execution = output["runtime_pain_batch_selfcheck_v1"]["repair_execution_v1"]
    repair_execution["repair_commands"] = []
    repair_execution["verify_commands"] = verify_cmds_input
    repair_execution["group_results"] = []
    repair_execution["manual_repair_applied"] = manual_repair_applied
    repair_execution["manual_repair_paths"] = manual_path_prefixes

    can_mark_resolved = False
    can_mark_all_groups = bool(selected_groups)
    write_result: dict[str, Any] = {"total_writes": 0, "success_writes": 0, "failed_writes": 0, "writes": []}
    group_repair_results: list[dict[str, Any]] = []
    all_repair_runs: list[dict[str, Any]] = []
    all_verify_runs: list[dict[str, Any]] = []
    per_group_blocked_reasons: list[str] = []

    if not selected_group:
        can_mark_all_groups = False
        repair_execution["blocked_reason"] = "no_pending_pain_group_selected"
    else:
        for group in selected_groups:
            group_key = str(group.get("pain_group_key", "") or "")
            group_topic = str(group.get("pain_topic", "") or "")
            manual_change_probe_enabled = False
            blocked_reason = ""
            if manual_repair_applied:
                if not manual_path_prefixes:
                    blocked_reason = "manual_repair_path_required"
                else:
                    manual_change_probe_enabled = True
                    group_repair_commands = ["true"]
                    repair_execution["repair_commands"].append("true")
            else:
                blocked_reason = "manual_repair_required_apply_patch"

            if blocked_reason:
                per_group_blocked_reasons.append(blocked_reason)
                can_mark_all_groups = False
                group_repair_results.append(
                    {
                        "group_key": group_key,
                        "pain_topic": group_topic,
                        "repair_commands": [],
                        "verify_commands": list(verify_cmds_input),
                        "repair_result": {
                            "total_commands": 0,
                            "success_commands": 0,
                            "failed_commands": 0,
                            "all_succeeded": False,
                            "runs": [],
                            "change_detection_supported": False,
                            "all_changed_paths": [],
                            "all_changed_path_count": 0,
                        },
                        "verify_result": {
                            "total_commands": 0,
                            "success_commands": 0,
                            "failed_commands": 0,
                            "all_succeeded": False,
                            "runs": [],
                            "change_detection_supported": False,
                            "all_changed_paths": [],
                            "all_changed_path_count": 0,
                        },
                        "can_mark_group_resolved": False,
                        "blocked_reason": blocked_reason,
                        "write_result": {
                            "total_writes": 0,
                            "success_writes": 0,
                            "failed_writes": 0,
                            "writes": [
                                {
                                    "group_key": group_key,
                                    "status": "skipped",
                                    "error": blocked_reason,
                                }
                            ],
                        },
                    }
                )
                continue

            repair_result = execute_command_list(
                commands=group_repair_commands,
                timeout_sec=max(1, int(args.repair_timeout_sec)),
                workdir=repair_workdir,
                change_detection_root=repair_workdir,
            )
            verify_result = (
                execute_command_list(
                    commands=verify_cmds_input,
                    timeout_sec=max(1, int(args.repair_timeout_sec)),
                    workdir=repair_workdir,
                    change_detection_root=repair_workdir,
                )
                if verify_cmds_input
                else {
                    "total_commands": 0,
                    "success_commands": 0,
                    "failed_commands": 0,
                    "all_succeeded": True,
                    "runs": [],
                    "change_detection_supported": False,
                    "all_changed_paths": [],
                    "all_changed_path_count": 0,
                }
            )
            if manual_change_probe_enabled:
                manual_probe = detect_preexisting_changes(
                    change_detection_root=repair_workdir,
                    timeout_sec=max(1, int(args.repair_timeout_sec)),
                )
                manual_paths = _filter_changed_paths(
                    manual_probe.get("all_changed_paths", []),
                    manual_path_prefixes,
                    repo_root=str(manual_probe.get("repo_root", "") or ""),
                )
                merged_paths = set(str(x) for x in (repair_result.get("all_changed_paths", []) or []))
                merged_paths.update(manual_paths)
                repair_result["all_changed_paths"] = sorted(merged_paths)
                repair_result["all_changed_path_count"] = len(merged_paths)
                repair_result["change_detection_supported"] = bool(repair_result.get("change_detection_supported", False)) or bool(
                    manual_probe.get("change_detection_supported", False)
                )
                repair_result["manual_preexisting_change_probe"] = {
                    "enabled": True,
                    "manual_repair_paths": manual_path_prefixes,
                    "repo_root": str(manual_probe.get("repo_root", "") or ""),
                    "matched_changed_paths": list(manual_paths),
                    "matched_changed_path_count": len(manual_paths),
                }
            all_repair_runs.append(repair_result)
            all_verify_runs.append(verify_result)
            repair_changed_files = int(repair_result.get("all_changed_path_count", 0) or 0)
            verify_changed_files = int(verify_result.get("all_changed_path_count", 0) or 0)
            change_detected = (repair_changed_files + verify_changed_files) > 0
            change_detection_supported = bool(repair_result.get("change_detection_supported", False)) or bool(
                verify_result.get("change_detection_supported", False)
            )

            can_mark_group_resolved = (
                bool(repair_result.get("all_succeeded", False))
                and bool(verify_result.get("all_succeeded", False))
                and change_detection_supported
                and change_detected
            )
            preflight_reason_codes = _dedupe_ordered_items(
                [
                    str(x)
                    for x in (
                        (repair_result.get("preflight_reason_codes", []) if isinstance(repair_result.get("preflight_reason_codes", []), list) else [])
                        + (verify_result.get("preflight_reason_codes", []) if isinstance(verify_result.get("preflight_reason_codes", []), list) else [])
                    )
                ]
            )
            if can_mark_group_resolved:
                group_blocked_reason = ""
            elif preflight_reason_codes:
                group_blocked_reason = f"preflight_blocked:{preflight_reason_codes[0]}"
            elif not change_detection_supported:
                group_blocked_reason = "repair_change_detection_not_available"
            elif not change_detected:
                group_blocked_reason = "repair_no_file_changes_detected"
            else:
                group_blocked_reason = "repair_or_verify_failed"

            per_group_blocked_reasons.append(group_blocked_reason) if group_blocked_reason else None
            if group_blocked_reason:
                can_mark_all_groups = False

            group_write_result: dict[str, Any] = {
                "total_writes": 0,
                "success_writes": 0,
                "failed_writes": 0,
                "writes": [],
            }
            if can_mark_group_resolved:
                group_write_result = resolve_group_batch(
                    run_memory_runtime=_run_memory_runtime,
                    memory_runtime=memory_runtime,
                    session_id=str(args.session_id or "").strip() or _latest_session_id(Path(args.history_path).expanduser()),
                    thread_id=str(args.thread_id or "").strip(),
                    target_groups=[group],
                    resolved_by=str(args.resolved_by or "2-Task-runtime-selfcheck"),
                    turn_id=str(args.turn_id or "runtime-pain-batch"),
                    dry_run=bool(args.dry_run),
                )
            else:
                group_write_result = {
                    "total_writes": 0,
                    "success_writes": 0,
                    "failed_writes": len(group.get("optimization_ids", []) or 0),
                    "writes": [
                        {
                            "group_key": group_key,
                            "status": "skipped",
                            "error": group_blocked_reason,
                        }
                    ],
                }

            # Normalize write result for groups where write back is expected but got zero outputs
            # (e.g., dry-run without selected ids or execution anomalies).
            if group_write_result.get("failed_writes", 0) > 0:
                can_mark_all_groups = False
                if not group_blocked_reason:
                    group_blocked_reason = "repair_writeback_failed"
                per_group_blocked_reasons.append(group_blocked_reason)
                if not group_write_result.get("writes"):
                    group_write_result = {
                        "total_writes": 0,
                        "success_writes": 0,
                        "failed_writes": len(group.get("optimization_ids", [])),
                        "writes": [
                            {
                                "group_key": group_key,
                                "status": "error",
                                "error": group_blocked_reason,
                            }
                        ],
                    }

            # accumulate grouped writes first
            write_result["writes"].extend(group_write_result.get("writes", []))
            write_result["total_writes"] += int(group_write_result.get("total_writes", 0))
            write_result["success_writes"] += int(group_write_result.get("success_writes", 0))
            write_result["failed_writes"] += int(group_write_result.get("failed_writes", 0))

            group_repair_results.append(
                {
                    "group_key": group_key,
                    "pain_topic": group_topic,
                    "repair_commands": list(group_repair_commands),
                    "verify_commands": list(verify_cmds_input),
                    "repair_result": repair_result,
                    "verify_result": verify_result,
                    "can_mark_group_resolved": bool(can_mark_group_resolved),
                    "blocked_reason": group_blocked_reason,
                    "write_result": group_write_result,
                }
            )

            if repair_result.get("failed_commands", 0) > 0 or verify_result.get("failed_commands", 0) > 0:
                can_mark_all_groups = False

        repair_execution["repair_result"] = _sum_execution_results(all_repair_runs)
        repair_execution["verify_result"] = _sum_execution_results(all_verify_runs) if verify_cmds_input else {
            "total_commands": 0,
            "success_commands": 0,
            "failed_commands": 0,
            "all_succeeded": True,
            "runs": [],
            "change_detection_supported": False,
            "all_changed_paths": [],
            "all_changed_path_count": 0,
        }
        repair_execution["group_results"] = group_repair_results
        repair_execution["repair_commands"] = _dedupe_ordered_items(repair_execution.get("repair_commands", []))
        if can_mark_all_groups and not per_group_blocked_reasons:
            repair_execution["blocked_reason"] = ""
        else:
            repair_execution["blocked_reason"] = _dedupe_ordered_items([str(x) for x in per_group_blocked_reasons if str(x).strip()])[0]
            if not repair_execution["blocked_reason"]:
                repair_execution["blocked_reason"] = "repair_not_completed"
        can_mark_resolved = can_mark_all_groups

    repair_execution["can_mark_resolved"] = can_mark_resolved and bool(selected_group)
    if bool(selected_group) and not can_mark_resolved:
        repair_execution["blocked_reason"] = repair_execution.get("blocked_reason") or "repair_not_completed"

    session_id = str(args.session_id or "").strip() or _latest_session_id(Path(args.history_path).expanduser())
    if repair_execution["can_mark_resolved"] and not session_id:
        output["status"] = "error"
        write_result = {"error": "missing_session_id_for_repair"}
        repair_execution["can_mark_resolved"] = False
        repair_execution["blocked_reason"] = "missing_session_id_for_repair"
        per_group_blocked_reasons.append("missing_session_id_for_repair")

    if isinstance(write_result.get("writes", []), list) and isinstance(write_result.get("error", None), str):
        # keep error form for hard-blocking path while retaining expected writeback schema.
        write_result = {
            "total_writes": 0,
            "success_writes": 0,
            "failed_writes": 0,
            "writes": [],
            "error": str(write_result.get("error")),
        }

    output["runtime_pain_batch_selfcheck_v1"]["repair_writeback"]["result"] = write_result
    output["runtime_pain_batch_selfcheck_v1"]["repair_writeback"]["target_group_count"] = len(selected_group_keys)
    output["runtime_pain_batch_selfcheck_v1"]["repair_writeback"]["session_id"] = session_id

    # Refresh queue to reflect unresolved items for next round.
    refreshed_queue = _queue_items(
        memory_runtime=memory_runtime,
        max_results=max(1, int(args.max_results)),
        include_resolved=bool(args.include_resolved),
        session_scope_mode=str(args.session_scope_mode or "auto"),
        thread_id=str(args.thread_id or "").strip(),
    )
    output["runtime_pain_batch_selfcheck_v1"]["post_repair_queue_summary"] = {
        "total_items": int(refreshed_queue.get("total_items", 0) or 0),
        "pending_items": int(refreshed_queue.get("pending_items", 0) or 0),
        "resolved_items": int(refreshed_queue.get("resolved_items", 0) or 0),
    }
    refreshed_items = refreshed_queue.get("items", []) if isinstance(refreshed_queue.get("items", []), list) else []
    refreshed_grouped = _group_items(refreshed_items)
    refreshed_groups = refreshed_grouped.get("groups", []) if isinstance(refreshed_grouped.get("groups", []), list) else []
    next_group_after_repair = select_current_group(groups=refreshed_groups, requested_keys=set())
    no_more_pending = len(pending_groups(refreshed_groups)) == 0
    output["runtime_pain_batch_selfcheck_v1"]["next_pain_v1"] = compact_group(next_group_after_repair)
    output["runtime_pain_batch_selfcheck_v1"]["all_pain_resolved_v1"] = no_more_pending
    output["runtime_pain_batch_selfcheck_v1"]["completion_message_v1"] = build_completion_message(
        next_group=next_group_after_repair,
        all_resolved=no_more_pending,
    )

    if int(write_result.get("failed_writes", 0) or 0) > 0:
        output["status"] = "partial"

    _emit_report_only_output(run_id=run_id, mode=mode, output=output)
    return 0 if output["status"] in {"ok", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
