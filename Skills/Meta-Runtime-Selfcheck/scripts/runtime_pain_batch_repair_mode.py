from __future__ import annotations

import argparse
from pathlib import Path

from runtime_pain_batch_repair_support import (
    empty_command_result,
    empty_write_result,
    filter_changed_paths,
    normalize_manual_path_prefixes,
    sum_execution_results,
)
from runtime_pain_repair import (
    build_completion_message,
    compact_group,
    detect_preexisting_changes,
    execute_command_list,
    pending_groups,
    resolve_group_batch,
    select_current_group,
    select_current_groups,
)
from runtime_pain_types import (
    CommandExecutionResult,
    RepairWriteResult,
    RuntimePainBatchOutput,
    RuntimePainGroup,
)
from runtime_pain_batch_support import (
    _dedupe_ordered_items,
    _group_items,
    _latest_session_id,
    _queue_items,
    _run_memory_runtime,
)


def apply_repair_mode(
    *,
    args: argparse.Namespace,
    output: RuntimePainBatchOutput,
    memory_runtime: Path,
    grouped_rows: list[RuntimePainGroup],
    requested_keys: list[str],
) -> None:
    payload = output.get("runtime_pain_batch_selfcheck_v1", {})
    if not isinstance(payload, dict):
        raise ValueError("runtime_pain_batch_selfcheck_v1 payload must be a dict")

    groups = grouped_rows
    selected_groups = select_current_groups(groups=groups, requested_keys=requested_keys)
    selected_group = selected_groups[0] if selected_groups else {}
    selected_group_key = str(selected_group.get("pain_group_key", "") or "")
    selected_group_keys = [str(group.get("pain_group_key", "") or "") for group in selected_groups]
    verify_cmds_input = [str(x).strip() for x in (args.verify_cmd or []) if str(x).strip()]
    repair_workdir = str(args.repair_workdir or "").strip()
    manual_repair_applied = bool(args.manual_repair_applied)
    manual_path_prefixes = normalize_manual_path_prefixes([str(x) for x in (args.manual_repair_path or [])])

    repair_execution = payload["repair_execution_v1"]
    if not isinstance(repair_execution, dict):
        raise ValueError("repair_execution_v1 payload must be a dict")
    repair_execution["repair_commands"] = []
    repair_execution["verify_commands"] = verify_cmds_input
    repair_execution["group_results"] = []
    repair_execution["manual_repair_applied"] = manual_repair_applied
    repair_execution["manual_repair_paths"] = manual_path_prefixes

    can_mark_resolved = False
    can_mark_all_groups = bool(selected_groups)
    write_result = empty_write_result()
    group_repair_results: list[dict[str, object]] = []
    all_repair_runs: list[CommandExecutionResult] = []
    all_verify_runs: list[CommandExecutionResult] = []
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
                    group_repair_commands: list[str] = []
                else:
                    manual_change_probe_enabled = True
                    group_repair_commands = ["true"]
                    repair_execution["repair_commands"].append("true")
            else:
                blocked_reason = "manual_repair_required_apply_patch"
                group_repair_commands = []

            if blocked_reason:
                per_group_blocked_reasons.append(blocked_reason)
                can_mark_all_groups = False
                group_repair_results.append(
                    {
                        "group_key": group_key,
                        "pain_topic": group_topic,
                        "repair_commands": [],
                        "verify_commands": list(verify_cmds_input),
                        "repair_result": empty_command_result(all_succeeded=False),
                        "verify_result": empty_command_result(all_succeeded=False),
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
                else empty_command_result(all_succeeded=True)
            )

            if manual_change_probe_enabled:
                manual_probe = detect_preexisting_changes(
                    change_detection_root=repair_workdir,
                    timeout_sec=max(1, int(args.repair_timeout_sec)),
                )
                manual_paths = filter_changed_paths(
                    manual_probe.get("all_changed_paths", []),
                    manual_path_prefixes,
                    repo_root=str(manual_probe.get("repo_root", "") or ""),
                )
                merged_paths = set(str(x) for x in repair_result.get("all_changed_paths", []))
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
                        list(repair_result.get("preflight_reason_codes", []))
                        + list(verify_result.get("preflight_reason_codes", []))
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

            if group_blocked_reason:
                per_group_blocked_reasons.append(group_blocked_reason)
                can_mark_all_groups = False

            if can_mark_group_resolved:
                group_write_result = resolve_group_batch(
                    run_memory_runtime=_run_memory_runtime,
                    memory_runtime=memory_runtime,
                    session_id=str(args.session_id or "").strip() or _latest_session_id(Path(args.history_path).expanduser()),
                    thread_id=str(args.thread_id or "").strip(),
                    target_groups=[group],
                    resolved_by=str(args.resolved_by or "Meta-Runtime-Selfcheck"),
                    turn_id=str(args.turn_id or "runtime-pain-batch"),
                    dry_run=bool(args.dry_run),
                )
            else:
                group_write_result = {
                    "total_writes": 0,
                    "success_writes": 0,
                    "failed_writes": len(group.get("optimization_ids", [])),
                    "writes": [
                        {
                            "group_key": group_key,
                            "status": "skipped",
                            "error": group_blocked_reason,
                        }
                    ],
                }

            if int(group_write_result.get("failed_writes", 0) or 0) > 0:
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

            write_result["writes"].extend(group_write_result.get("writes", []))
            write_result["total_writes"] += int(group_write_result.get("total_writes", 0) or 0)
            write_result["success_writes"] += int(group_write_result.get("success_writes", 0) or 0)
            write_result["failed_writes"] += int(group_write_result.get("failed_writes", 0) or 0)

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

            if int(repair_result.get("failed_commands", 0) or 0) > 0 or int(verify_result.get("failed_commands", 0) or 0) > 0:
                can_mark_all_groups = False

        repair_execution["repair_result"] = sum_execution_results(all_repair_runs)
        repair_execution["verify_result"] = sum_execution_results(all_verify_runs) if verify_cmds_input else empty_command_result(
            all_succeeded=True
        )
        repair_execution["group_results"] = group_repair_results
        repair_execution["repair_commands"] = _dedupe_ordered_items(repair_execution.get("repair_commands", []))
        if can_mark_all_groups and not per_group_blocked_reasons:
            repair_execution["blocked_reason"] = ""
        else:
            blocked_values = _dedupe_ordered_items([str(x) for x in per_group_blocked_reasons if str(x).strip()])
            repair_execution["blocked_reason"] = blocked_values[0] if blocked_values else "repair_not_completed"
        can_mark_resolved = can_mark_all_groups

    repair_execution["can_mark_resolved"] = can_mark_resolved and bool(selected_group)
    if bool(selected_group) and not can_mark_resolved:
        repair_execution["blocked_reason"] = repair_execution.get("blocked_reason") or "repair_not_completed"

    session_id = str(args.session_id or "").strip() or _latest_session_id(Path(args.history_path).expanduser())
    if repair_execution["can_mark_resolved"] and not session_id:
        output["status"] = "error"
        write_result = {
            "total_writes": 0,
            "success_writes": 0,
            "failed_writes": 0,
            "writes": [],
            "error": "missing_session_id_for_repair",
        }
        repair_execution["can_mark_resolved"] = False
        repair_execution["blocked_reason"] = "missing_session_id_for_repair"

    payload["repair_writeback"]["result"] = write_result
    payload["repair_writeback"]["target_group_count"] = len(selected_group_keys)
    payload["repair_writeback"]["session_id"] = session_id

    refreshed_queue = _queue_items(
        memory_runtime=memory_runtime,
        max_results=max(1, int(args.max_results)),
        include_resolved=bool(args.include_resolved),
        session_scope_mode=str(args.session_scope_mode or "auto"),
        thread_id=str(args.thread_id or "").strip(),
    )
    payload["post_repair_queue_summary"] = {
        "total_items": int(refreshed_queue.get("total_items", 0) or 0),
        "pending_items": int(refreshed_queue.get("pending_items", 0) or 0),
        "resolved_items": int(refreshed_queue.get("resolved_items", 0) or 0),
    }
    refreshed_items = refreshed_queue.get("items", []) if isinstance(refreshed_queue.get("items", []), list) else []
    refreshed_grouped = _group_items(refreshed_items)
    refreshed_groups = refreshed_grouped.get("groups", []) if isinstance(refreshed_grouped.get("groups", []), list) else []
    next_group_after_repair = select_current_group(groups=refreshed_groups, requested_keys=set())
    no_more_pending = len(pending_groups(refreshed_groups)) == 0
    payload["next_pain_v1"] = compact_group(next_group_after_repair)
    payload["all_pain_resolved_v1"] = no_more_pending
    payload["completion_message_v1"] = build_completion_message(
        next_group=next_group_after_repair,
        all_resolved=no_more_pending,
    )

    if int(write_result.get("failed_writes", 0) or 0) > 0:
        output["status"] = "partial"
