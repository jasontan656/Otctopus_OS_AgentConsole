from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from runtime_pain_observability import normalize_text
from runtime_pain_repair_candidates import extract_group_repair_commands
from runtime_pain_repair_exec import detect_preexisting_changes, execute_command_list


def resolve_group_batch(
    *,
    run_memory_runtime: Callable[[Path, list[str]], dict[str, Any]],
    memory_runtime: Path,
    session_id: str,
    thread_id: str,
    target_groups: list[dict[str, Any]],
    resolved_by: str,
    turn_id: str,
    dry_run: bool,
) -> dict[str, Any]:
    writes: list[dict[str, Any]] = []
    for group in target_groups:
        group_key = str(group.get("pain_group_key", "") or "")
        group_topic = str(group.get("pain_topic", "") or "")
        for row in group.get("optimization_ids", []):
            if not isinstance(row, dict):
                continue

            opt_id = str(row.get("optimization_id", "") or "").strip()
            if not opt_id or bool(row.get("is_resolved", False)):
                continue

            item_session_id = str(row.get("session_id", "") or session_id).strip()
            item_thread_id = str(row.get("thread_id", "") or thread_id).strip()
            if not item_session_id:
                writes.append(
                    {
                        "optimization_id": opt_id,
                        "group_key": group_key,
                        "status": "error",
                        "error": "missing_session_id_for_repair",
                    }
                )
                continue

            summary = normalize_text(f"batch_resolved_by_group:{group_key}; topic={group_topic}", limit=260)
            if dry_run:
                writes.append(
                    {
                        "optimization_id": opt_id,
                        "group_key": group_key,
                        "status": "dry_run",
                        "resolution_status": "resolved",
                        "resolution_summary": summary,
                        "session_id": item_session_id,
                        "thread_id": item_thread_id,
                    }
                )
                continue

            args = [
                "optimization-resolve",
                "--session-id",
                item_session_id,
                "--optimization-id",
                opt_id,
                "--resolution-status",
                "resolved",
                "--resolution-summary",
                summary,
                "--resolved-by",
                resolved_by,
                "--surface",
                "cli",
                "--turn-id",
                turn_id,
            ]
            if item_thread_id:
                args.extend(["--thread-id", item_thread_id])

            try:
                out = run_memory_runtime(memory_runtime, args)
                writes.append(
                    {
                        "optimization_id": opt_id,
                        "group_key": group_key,
                        "status": str(out.get("status", "ok") or "ok"),
                        "resolution_status": str(out.get("resolution_status", "resolved") or "resolved"),
                        "memory_entry_id": str(out.get("memory_entry_id", "") or ""),
                        "memory_path": str(out.get("memory_path", "") or ""),
                        "session_id": item_session_id,
                        "thread_id": item_thread_id,
                    }
                )
            except Exception as exc:
                writes.append(
                    {
                        "optimization_id": opt_id,
                        "group_key": group_key,
                        "status": "error",
                        "error": normalize_text(str(exc), limit=280),
                    }
                )

    success = sum(1 for row in writes if str(row.get("status", "")).lower() in {"ok", "dry_run"})
    failed = sum(1 for row in writes if str(row.get("status", "")).lower() not in {"ok", "dry_run"})
    return {
        "total_writes": len(writes),
        "success_writes": success,
        "failed_writes": failed,
        "writes": writes,
    }


def pending_groups(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pending: list[dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        if int(group.get("pending_items", 0) or 0) <= 0:
            continue
        pending.append(group)
    return pending


def _ordered_request_keys(requested_keys: list[str] | tuple[str, ...] | set[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for key in requested_keys:
        normalized = str(key or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def select_current_groups(*, groups: list[dict[str, Any]], requested_keys: list[str] | set[str] | tuple[str, ...]) -> list[dict[str, Any]]:
    pending = pending_groups(groups)
    if not pending:
        return []

    requested = _ordered_request_keys(requested_keys)
    if not requested:
        return [pending[0]]

    if "all" in requested:
        return pending

    groups_by_key = {str(group.get("pain_group_key", "") or "").strip(): group for group in pending}
    return [groups_by_key[key] for key in requested if key in groups_by_key]


def select_current_group(*, groups: list[dict[str, Any]], requested_keys: set[str]) -> dict[str, Any]:
    selected = select_current_groups(groups=groups, requested_keys=requested_keys)
    return selected[0] if selected else {}


def find_next_group(
    *,
    groups: list[dict[str, Any]],
    selected_group_key: str = "",
    selected_group_keys: list[str] | set[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    skip_keys = set(_ordered_request_keys(selected_group_keys or []))
    selected = str(selected_group_key or "").strip()
    if selected:
        skip_keys.add(selected)

    for group in pending_groups(groups):
        key = str(group.get("pain_group_key", "") or "").strip()
        if key and key in skip_keys:
            continue
        return group
    return {}


def compact_group(group: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(group, dict):
        return {}
    return {
        "pain_group_key": str(group.get("pain_group_key", "") or ""),
        "pain_topic": str(group.get("pain_topic", "") or ""),
        "pending_items": int(group.get("pending_items", 0) or 0),
        "priority_top": str(group.get("priority_top", "") or ""),
        "problem_statement": str(group.get("problem_statement", "") or ""),
        "analysis": str(group.get("analysis", "") or ""),
        "remediation_plan": str(group.get("remediation_plan", "") or ""),
        "latest_updated_at": str(group.get("latest_updated_at", "") or ""),
    }


def build_completion_message(*, next_group: dict[str, Any], all_resolved: bool) -> str:
    if all_resolved:
        return "全部修复，没有其他痛点可修了。"

    key = str(next_group.get("pain_group_key", "") or "").strip()
    topic = str(next_group.get("pain_topic", "") or "").strip()
    if not key:
        return "仍有未修复痛点，请继续处理当前队首痛点。"
    if not topic:
        return f"下一个痛点：{key}。"
    return f"下一个痛点：{key}（{topic}）。"
