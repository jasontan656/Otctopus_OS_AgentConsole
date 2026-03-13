#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_pain_observability import attach_observability_logs, new_run_id
from runtime_pain_focus import build_focus_group
from runtime_pain_repair import (
    build_completion_message,
    compact_group,
    find_next_group,
    pending_groups,
    select_current_groups,
)
from runtime_pain_batch_repair_mode import apply_repair_mode
from runtime_pain_types import RuntimePainBatchOutput
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


def _emit_report_only_output(*, run_id: str, mode: str, output: RuntimePainBatchOutput) -> None:
    attach_observability_logs(run_id=run_id, mode=mode, output=output)
    report_only_output = _build_report_only_output(
        status=str(output.get("status", "ok") or "ok"),
        payload=output["runtime_pain_batch_selfcheck_v1"],
    )
    print(json.dumps(report_only_output, ensure_ascii=False, indent=2, sort_keys=True))


def run_with_args(args: argparse.Namespace) -> int:
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
    output: RuntimePainBatchOutput = {
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

    apply_repair_mode(
        args=args,
        output=output,
        memory_runtime=memory_runtime,
        grouped_rows=grouped_rows,
        requested_keys=requested_keys,
    )

    _emit_report_only_output(run_id=run_id, mode=mode, output=output)
    return 0 if output["status"] in {"ok", "partial"} else 1
