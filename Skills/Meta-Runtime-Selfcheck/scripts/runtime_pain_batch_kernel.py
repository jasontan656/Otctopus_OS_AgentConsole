#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from runtime_pain_observability import (
    HUMAN_LOG_NAME,
    HUMAN_RENDERER,
    HUMAN_SUMMARY_KEY,
    MACHINE_LOG_NAME,
    attach_observability_logs,
    new_run_id,
    normalize_text,
)
from runtime_pain_focus import build_focus_group
from runtime_pain_narrative import build_narrative_package
from runtime_pain_repair import (
    build_completion_message,
    compact_group,
    execute_command_list,
    extract_group_repair_commands,
    find_next_group,
    pending_groups,
    resolve_group_batch,
    select_current_groups,
    select_current_group,
)

REPAIR_TOKEN = "修复"
DIAGNOSE_TOKEN = ">"


def _default_codex_home() -> Path:
    script_path = Path(__file__).resolve()
    repo_root = next((parent for parent in script_path.parents if parent.name == "octopus-os-agent-console"), None)
    if repo_root is not None:
        local_codex_home = (repo_root.parent / ".codex").resolve()
        if local_codex_home.exists():
            return local_codex_home
    env_home = os.environ.get("CODEX_HOME", "").strip()
    if env_home:
        return Path(env_home).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


CODEX_HOME = _default_codex_home()
DEFAULT_MEMORY_RUNTIME = str(os.environ.get("CODEX_RUNTIME_PAIN_PROVIDER", "")).strip()
DEFAULT_HISTORY = (CODEX_HOME / "history.jsonl").resolve()
FORCED_SCOPE_MODE = "all_threads"
FORCED_SCOPE_THREAD_ID = "all_threads"
EVENT_COMMAND_PREVIEW_LIMIT = 420
EVENT_COMMAND_SIGNATURE_LIMIT = 360
EVIDENCE_SAMPLE_LIMIT = 3
TIMELINE_LIMIT = 5
BACKTICK = chr(96)

def _sanitize_text_for_event(value: str, *, limit: int) -> str:
    text = str(value or "").strip()
    return normalize_text(text, limit=limit)

def _detect_mode(*, mode: str, raw_tokens: list[str]) -> str:
    normalized = str(mode or "auto").strip().lower()
    if normalized == "repair":
        return "repair"
    if normalized == "diagnose":
        return "diagnose"
    for token in raw_tokens:
        if str(token).strip() == REPAIR_TOKEN:
            return "repair"
        if str(token).strip() == DIAGNOSE_TOKEN:
            return "diagnose"
    return "diagnose"


def _normalize_signature_for_grouping(signature: str) -> str:
    s = str(signature or "").strip()
    if not s:
        return s

    if "|runtime|" in s:
        s = s.split("|runtime|", 1)[1]
    if s.startswith("tool_failure_any|"):
        parts = s.split("|", 1)
        s = parts[1] if len(parts) > 1 else s
    if s.startswith("exec_command|"):
        s = s.split("|", 1)[1]

    # 去掉常见占位符与可变片段，保持命令骨架。
    s = re.sub(r"<[^>]+>", "<ARG>", s)
    s = re.sub(rf"{BACKTICK}[^{BACKTICK}]*{BACKTICK}", " <CMD> ", s)
    s = re.sub(r"\$[A-Za-z_][A-Za-z0-9_]*", " <ENV> ", s)
    s = re.sub(r"\b\d+[A-Za-z]?\b", " <NUM> ", s)
    s = re.sub(r"\b[0-9a-fA-F]{12,}\b", " <ID> ", s)
    s = re.sub(r"(?<![\w./])(?:/|\.\./|\./|~[/\w]).*?(?=\s|$)", " <PATH> ", s)
    s = re.sub(r"\s+", " ", s).strip()

    return s


def _derive_group_signature(row: dict[str, Any]) -> str:
    source_event = row.get("source_event", {}) if isinstance(row.get("source_event", {}), dict) else {}
    kind = str(row.get("kind", "") or "").strip()
    tool_name = str(source_event.get("tool_name", "") or "").strip()
    trigger_node = str(source_event.get("trigger_node", "") or "").strip()
    trigger_script = str(source_event.get("trigger_script", "") or "").strip()

    raw_signature = (
        source_event.get("command_signature")
        or row.get("pain_signature")
        or str(row.get("pain_topic", "") or "")
    )
    normalized = _normalize_signature_for_grouping(str(raw_signature))
    base = f"{kind}|{tool_name}|{trigger_node}|{trigger_script}|{normalized}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def _latest_session_id(history_path: Path) -> str:
    if not history_path.exists():
        return ""
    latest = ""
    with history_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            try:
                payload = json.loads(raw)
            except Exception:
                continue
            sid = str(payload.get("session_id", "") or "").strip()
            if sid:
                latest = sid
    return latest

def _run_memory_runtime(memory_runtime: Path, args: list[str]) -> dict[str, Any]:
    cmd = [sys.executable, str(memory_runtime), *args]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(memory_runtime.parent.resolve()),
    )
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise RuntimeError(
            f"memory_runtime_failed rc={proc.returncode}; cmd={' '.join(cmd)}; stderr={stderr or '<empty>'}; stdout={stdout or '<empty>'}"
        )
    if not stdout:
        raise RuntimeError(f"memory_runtime_empty_output; cmd={' '.join(cmd)}")

    for line in reversed(stdout.splitlines()):
        candidate = line.strip()
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except Exception:
            continue
    raise RuntimeError(f"memory_runtime_non_json_output; cmd={' '.join(cmd)}; stdout={stdout[:280]}")


def _queue_items(
    *,
    memory_runtime: Path,
    max_results: int,
    include_resolved: bool,
    session_scope_mode: str,
    thread_id: str,
) -> dict[str, Any]:
    # Reverse-upgrade policy: always consume pain points across all recorded threads.
    _ = session_scope_mode, thread_id
    args = [
        "optimization-list",
        "--max-results",
        str(max(1, int(max_results))),
        "--session-scope-mode",
        FORCED_SCOPE_MODE,
        "--thread-id",
        FORCED_SCOPE_THREAD_ID,
    ]
    args.append("--include-resolved" if include_resolved else "--no-include-resolved")
    out = _run_memory_runtime(memory_runtime, args)
    queue = out.get("optimization_queue_v1", {}) if isinstance(out, dict) else {}
    if not isinstance(queue, dict):
        queue = {}
    return queue

def _action_for_group(kinds: set[str], tool_names: set[str]) -> str:
    prioritized_actions = (
        ("tool_failure_any", "为同节点增加失败分支处理与预检，失败后立即分流而不是重复调用"),
        ("trial_and_error_loop", "为同签名动作增加决策阈值与重试上限，避免犹豫循环"),
        ("phase_incomplete", "补齐阶段完成门禁与验收条件，避免阶段半完成状态反复出现"),
        ("blocker_recovery", "加入阻塞回退路径与降级动作，确保阻塞后有可执行下一步"),
    )
    matched_action = next((action for key, action in prioritized_actions if key in kinds), "")
    if matched_action:
        return matched_action
    tool_hint = ",".join(sorted(t for t in tool_names if t)[:3])
    return (
        f"围绕工具 {tool_hint} 增加节点级稳定性策略（预检/重试/失败处理）"
        if tool_hint
        else "按触发节点补齐稳定化策略（预检、失败处理、回退路径）"
    )

def _priority_rank(value: str) -> int:
    return {"p0": 3, "p1": 2, "p2": 1}.get(str(value or "").strip().lower(), 0)

def _top_counts(values: list[str], *, limit: int = 5) -> list[dict[str, Any]]:
    counter = Counter(str(v).strip() for v in values if str(v).strip())
    return [{"value": key, "count": count} for key, count in counter.most_common(max(1, int(limit)))]

def _event_sort_key(event: dict[str, Any]) -> tuple[int, int, str, str]:
    pending_rank = 1 if not bool(event.get("is_resolved", False)) else 0
    priority_rank = _priority_rank(str(event.get("priority", "p2") or "p2"))
    return (
        pending_rank,
        priority_rank,
        str(event.get("updated_at", "") or ""),
        str(event.get("optimization_id", "") or ""),
    )


def _normalize_ordered_keys(keys: list[str] | tuple[str, ...] | set[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for key in keys:
        normalized = str(key or "").strip()
        if not normalized or normalized in seen:
            continue
        ordered.append(normalized)
        seen.add(normalized)
    return ordered


def _dedupe_ordered_items(items: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in items:
        value = str(item or "").strip()
        if not value or value in seen:
            continue
        deduped.append(value)
        seen.add(value)
    return deduped

def _group_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, dict[str, Any]] = {}
    signature_to_group_key: dict[str, str] = {}
    for raw in items:
        if not isinstance(raw, dict):
            continue
        optimization_id = str(raw.get("optimization_id", "") or "").strip()
        if not optimization_id:
            continue

        pain_signature = str(raw.get("pain_signature", "") or "").strip()
        derived_group_key = _derive_group_signature(raw)
        pain_group_key = str(raw.get("pain_group_key", "") or "").strip()
        if not pain_group_key:
            pain_group_key = f"pg_{hashlib.sha256((pain_signature or derived_group_key).encode('utf-8')).hexdigest()[:16]}"
        canonical_key = signature_to_group_key.setdefault(derived_group_key, pain_group_key)
        pain_group_key = canonical_key
        if not pain_group_key.startswith("pg_"):
            pain_group_key = f"pg_{hashlib.sha256(pain_group_key.encode('utf-8')).hexdigest()[:16]}"
            signature_to_group_key[derived_group_key] = pain_group_key

        source_event = raw.get("source_event", {}) if isinstance(raw.get("source_event", {}), dict) else {}
        is_resolved = bool(raw.get("is_resolved", False))
        priority = str(raw.get("priority", "p2") or "p2").strip().lower()
        kind = str(raw.get("kind", "") or "").strip()
        tool_name = str(source_event.get("tool_name", "") or "").strip()
        trigger_node = str(source_event.get("trigger_node", "") or "").strip()
        trigger_script = str(source_event.get("trigger_script", "") or "").strip()

        bucket = grouped.setdefault(
            pain_group_key,
            {
                "pain_group_key": pain_group_key,
                "pain_topic": str(raw.get("pain_topic", "") or "").strip(),
                "group_signature": derived_group_key,
                "pain_consistency_hash": str(raw.get("pain_consistency_hash", "") or "").strip(),
                "pending_items": 0,
                "resolved_items": 0,
                "total_items": 0,
                "priority_top": "p2",
                "kinds": set(),
                "tool_names": set(),
                "trigger_nodes": set(),
                "trigger_scripts": set(),
                "citations": [],
                "optimization_ids": [],
                "events": [],
                "latest_updated_at": "",
            },
        )

        bucket["total_items"] = int(bucket["total_items"]) + 1
        if is_resolved:
            bucket["resolved_items"] = int(bucket["resolved_items"]) + 1
        else:
            bucket["pending_items"] = int(bucket["pending_items"]) + 1

        if priority in {"p0", "p1", "p2"}:
            p_rank = {"p0": 3, "p1": 2, "p2": 1}
            current = str(bucket["priority_top"])
            if p_rank[priority] >= p_rank.get(current, 0):
                bucket["priority_top"] = priority

        if kind:
            bucket["kinds"].add(kind)
        if tool_name:
            bucket["tool_names"].add(tool_name)
        if trigger_node:
            bucket["trigger_nodes"].add(trigger_node)
        if trigger_script:
            bucket["trigger_scripts"].add(trigger_script)

        citation = str(raw.get("citation", "") or "").strip()
        if citation:
            bucket["citations"].append(citation)
        source_citation = str(source_event.get("citation", "") or "").strip()
        if source_citation:
            bucket["citations"].append(source_citation)
        merged_citation = citation or source_citation

        updated_at = str(raw.get("updated_at", "") or "")
        title = normalize_text(str(raw.get("title", "") or ""), limit=180)
        suggested_action = normalize_text(str(raw.get("suggested_action", "") or ""), limit=200)
        summary = normalize_text(str(raw.get("summary", "") or ""), limit=240)
        why = normalize_text(str(raw.get("why", "") or ""), limit=180)
        command_preview = _sanitize_text_for_event(str(source_event.get("command_preview", "") or ""), limit=EVENT_COMMAND_PREVIEW_LIMIT)
        command_signature = _sanitize_text_for_event(str(source_event.get("command_signature", "") or ""), limit=EVENT_COMMAND_SIGNATURE_LIMIT)
        command_preview_raw = _sanitize_text_for_event(str(source_event.get("command_preview", "") or ""), limit=EVENT_COMMAND_PREVIEW_LIMIT)
        command_signature_raw = _sanitize_text_for_event(str(source_event.get("command_signature", "") or ""), limit=EVENT_COMMAND_SIGNATURE_LIMIT)
        outcome = normalize_text(str(source_event.get("outcome", "") or ""), limit=220)
        next_hint = normalize_text(str(source_event.get("next", "") or ""), limit=160)

        event_record = {
            "optimization_id": optimization_id,
            "is_resolved": is_resolved,
            "priority": priority,
            "kind": kind,
            "title": title,
            "suggested_action": suggested_action,
            "updated_at": updated_at,
            "tool_name": tool_name,
            "trigger_node": trigger_node,
            "trigger_script": trigger_script,
            "command_preview": command_preview,
            "command_signature": command_signature,
            "outcome": outcome,
            "summary": summary,
                "why": why,
                "next": next_hint,
                "citation": merged_citation,
                "command_preview_raw": command_preview_raw,
                "command_signature_raw": command_signature_raw,
            }
        bucket["optimization_ids"].append(
            {
                "optimization_id": optimization_id,
                "is_resolved": is_resolved,
                "priority": priority,
                "kind": kind,
                "title": title,
                "suggested_action": suggested_action,
                "updated_at": updated_at,
                "session_id": str(raw.get("session_id", "") or "").strip(),
                "thread_id": str(raw.get("thread_id", "") or "").strip(),
            }
        )
        bucket["events"].append(event_record)

        if updated_at >= str(bucket["latest_updated_at"]):
            bucket["latest_updated_at"] = updated_at

    groups_out: list[dict[str, Any]] = []
    for bucket in grouped.values():
        kinds = {str(v) for v in bucket["kinds"] if str(v)}
        tools = {str(v) for v in bucket["tool_names"] if str(v)}
        remediation_action = _action_for_group(kinds, tools)
        if not bucket["pain_topic"]:
            first_kind = next(iter(sorted(kinds)), "runtime_pain")
            first_tool = next(iter(sorted(tools)), "node")
            bucket["pain_topic"] = f"{first_kind}:{first_tool}"

        citations = sorted(set(str(x) for x in bucket["citations"] if str(x)))
        events = [row for row in bucket.get("events", []) if isinstance(row, dict)]
        events_sorted = sorted(events, key=_event_sort_key, reverse=True)

        evidence_samples = [
            {
                "optimization_id": str(event.get("optimization_id", "") or ""),
                "status": "resolved" if bool(event.get("is_resolved", False)) else "pending",
                "priority": str(event.get("priority", "p2") or "p2"),
                "kind": str(event.get("kind", "") or ""),
                "title": str(event.get("title", "") or ""),
                "suggested_action": str(event.get("suggested_action", "") or ""),
                "trigger_node": str(event.get("trigger_node", "") or ""),
                "trigger_script": str(event.get("trigger_script", "") or ""),
                "command_preview": str(event.get("command_preview", "") or ""),
                "tool_name": str(event.get("tool_name", "") or ""),
                "command_signature": str(event.get("command_signature", "") or ""),
                "outcome": str(event.get("outcome", "") or ""),
                "summary": str(event.get("summary", "") or ""),
                "why": str(event.get("why", "") or ""),
                "updated_at": str(event.get("updated_at", "") or ""),
                "citation": str(event.get("citation", "") or ""),
            }
            for event in events_sorted[:EVIDENCE_SAMPLE_LIMIT]
        ]
        timeline_v1 = [
            {
                "updated_at": str(event.get("updated_at", "") or ""),
                "optimization_id": str(event.get("optimization_id", "") or ""),
                "status": "resolved" if bool(event.get("is_resolved", False)) else "pending",
                "kind": str(event.get("kind", "") or ""),
                "trigger_node": str(event.get("trigger_node", "") or ""),
                "title": str(event.get("title", "") or ""),
                "citation": str(event.get("citation", "") or ""),
            }
            for event in sorted(events, key=lambda row: str(row.get("updated_at", "") or ""), reverse=True)[:TIMELINE_LIMIT]
        ]

        pending_items = int(bucket["pending_items"])
        resolved_items = int(bucket["resolved_items"])
        total_items = int(bucket["total_items"])
        pending_ratio = round(float(pending_items) / float(max(total_items, 1)), 3)

        trigger_nodes_sorted = sorted({str(v) for v in bucket["trigger_nodes"] if str(v)})
        trigger_scripts_sorted = sorted({str(v) for v in bucket["trigger_scripts"] if str(v)})
        tool_names_sorted = sorted(tools)
        kind_counts = _top_counts([str(event.get("kind", "") or "") for event in events], limit=6)
        node_counts = _top_counts([str(event.get("trigger_node", "") or "") for event in events], limit=5)
        script_counts = _top_counts([str(event.get("trigger_script", "") or "") for event in events], limit=5)
        tool_counts = _top_counts([str(event.get("tool_name", "") or "") for event in events], limit=5)

        problem_statement = (
            f"组 {bucket['pain_group_key']} 在 topic {bucket['pain_topic']} 下累计记录 {total_items} 次，"
            f"当前仍有 {pending_items} 条未修复，且最高优先级为 {bucket['priority_top']}。"
        )
        narrative_package = build_narrative_package(
            pain_group_key=str(bucket["pain_group_key"]),
            pain_topic=str(bucket["pain_topic"]),
            kinds=kinds,
            trigger_nodes=trigger_nodes_sorted,
            trigger_scripts=trigger_scripts_sorted,
            pending_items=pending_items,
            total_items=total_items,
            priority_top=str(bucket["priority_top"]),
            remediation_action=remediation_action,
            events_sorted=events_sorted,
        )
        root_cause_hypotheses = narrative_package.get("root_cause_hypotheses", [])
        if not isinstance(root_cause_hypotheses, list):
            root_cause_hypotheses = []
        action_plan_v1 = narrative_package.get("action_plan_v1", [])
        if not isinstance(action_plan_v1, list):
            action_plan_v1 = []
        acceptance_checks_v1 = narrative_package.get("acceptance_checks_v1", [])
        if not isinstance(acceptance_checks_v1, list):
            acceptance_checks_v1 = []
        repair_strategy_v2 = narrative_package.get("repair_strategy_v2", {})
        if not isinstance(repair_strategy_v2, dict):
            repair_strategy_v2 = {}
        manager_story_v1 = narrative_package.get("manager_story_v1", {})
        if not isinstance(manager_story_v1, dict):
            manager_story_v1 = {}
        meta_reasoningchain_v1 = narrative_package.get("meta_reasoningchain_v1", {})
        if not isinstance(meta_reasoningchain_v1, dict):
            meta_reasoningchain_v1 = {}

        impact_severity = "low"
        if str(bucket["priority_top"]) == "p0" or pending_items >= 5:
            impact_severity = "high"
        elif str(bucket["priority_top"]) == "p1" or pending_items >= 2:
            impact_severity = "medium"

        unknowns: list[str] = []
        if not any(str(event.get("citation", "") or "").strip() for event in events):
            unknowns.append("缺少 citation 锚点，回溯原始上下文成本较高。")
        if not any(str(event.get("trigger_node", "") or "").strip() for event in events):
            unknowns.append("缺少 trigger_node，无法精确定位修复节点。")
        if not any(str(event.get("command_signature", "") or "").strip() for event in events):
            unknowns.append("缺少 command_signature，难以做脚本级去重与复现。")

        diagnosis_card_v2 = {
            "problem_statement": problem_statement,
            "fact_summary_v1": {
                "pending_items": pending_items,
                "resolved_items": resolved_items,
                "total_items": total_items,
                "pending_ratio": pending_ratio,
                "evidence_total_items": len(events_sorted),
                "evidence_sample_items": len(evidence_samples),
                "timeline_total_items": len(events),
                "timeline_sample_items": len(timeline_v1),
                "priority_top": str(bucket["priority_top"]),
                "kind_counts": kind_counts,
                "trigger_node_counts": node_counts,
                "trigger_script_counts": script_counts,
                "tool_counts": tool_counts,
            },
            "fact_evidence_samples": evidence_samples,
            "timeline_v1": timeline_v1,
            "inference_summary_v1": {
                "root_cause_hypotheses": root_cause_hypotheses,
                "confidence_note": "基于 memory pain queue 的归并统计推断，需要结合代码路径二次验证。",
            },
            "impact_scope_v1": {
                "severity_estimate": impact_severity,
                "affected_tools": tool_names_sorted[:8],
                "affected_trigger_nodes": trigger_nodes_sorted[:8],
                "affected_trigger_scripts": trigger_scripts_sorted[:8],
                "blast_radius_hint": f"同组 pending 占比 {pending_ratio}，若不处理将继续污染后续自检信号。",
            },
            "action_plan_v1": action_plan_v1,
            "acceptance_checks_v1": acceptance_checks_v1,
            "repair_strategy_v2": repair_strategy_v2,
            "manager_story_v1": manager_story_v1,
            "meta_reasoningchain_v1": meta_reasoningchain_v1,
            "unknowns": unknowns,
        }

        inference_brief = root_cause_hypotheses[0]["hypothesis"] if root_cause_hypotheses else "需要进一步定位根因。"
        executive_summary = str(manager_story_v1.get("executive_summary", "") or "")
        groups_out.append(
            {
                "pain_group_key": bucket["pain_group_key"],
                "pain_topic": bucket["pain_topic"],
                "pain_consistency_hash": bucket["pain_consistency_hash"],
                "pending_items": pending_items,
                "resolved_items": resolved_items,
                "total_items": total_items,
                "priority_top": str(bucket["priority_top"]),
                "kinds": sorted(kinds),
                "tool_names": tool_names_sorted,
                "trigger_nodes": trigger_nodes_sorted,
                "trigger_scripts": trigger_scripts_sorted,
                "citations": citations[:12],
                "problem_statement": problem_statement,
                "analysis": f"[管理摘要] {executive_summary or '当前问题需要按组治理。'} [推断] {inference_brief}",
                "remediation_plan": remediation_action,
                "optimization_ids": bucket["optimization_ids"],
                "diagnosis_card_v2": diagnosis_card_v2,
                "latest_updated_at": str(bucket["latest_updated_at"]),
            }
        )

    groups_out.sort(
        key=lambda row: (
            int(row.get("pending_items", 0) or 0),
            {"p0": 3, "p1": 2, "p2": 1}.get(str(row.get("priority_top", "p2")), 0),
            str(row.get("latest_updated_at", "") or ""),
            str(row.get("pain_group_key", "") or ""),
        ),
        reverse=True,
    )
    return {
        "group_count": len(groups_out),
        "pending_group_count": sum(1 for row in groups_out if int(row.get("pending_items", 0) or 0) > 0),
        "resolved_group_count": sum(1 for row in groups_out if int(row.get("resolved_items", 0) or 0) > 0),
        "groups": groups_out,
    }


def _build_pain_inventory(
    *,
    groups: list[dict[str, Any]],
    focus_group_key: str,
) -> dict[str, Any]:
    topic_rollup: dict[str, dict[str, Any]] = {}
    group_rows: list[dict[str, Any]] = []
    total_records = 0
    total_pending = 0
    total_resolved = 0

    for row in groups:
        if not isinstance(row, dict):
            continue
        group_key = str(row.get("pain_group_key", "") or "")
        pain_topic = str(row.get("pain_topic", "") or "")
        total_items = int(row.get("total_items", 0) or 0)
        pending_items = int(row.get("pending_items", 0) or 0)
        resolved_items = int(row.get("resolved_items", 0) or 0)
        priority_top = str(row.get("priority_top", "") or "")

        total_records += total_items
        total_pending += pending_items
        total_resolved += resolved_items
        group_rows.append(
            {
                "pain_group_key": group_key,
                "pain_topic": pain_topic,
                "priority_top": priority_top,
                "total_records": total_items,
                "pending_records": pending_items,
                "resolved_records": resolved_items,
                "removable_records_if_group_resolved": pending_items,
                "is_focus_group": group_key == focus_group_key,
            }
        )

        topic_bucket = topic_rollup.setdefault(
            pain_topic,
            {
                "pain_topic": pain_topic,
                "group_count": 0,
                "total_records": 0,
                "pending_records": 0,
                "resolved_records": 0,
            },
        )
        topic_bucket["group_count"] = int(topic_bucket["group_count"]) + 1
        topic_bucket["total_records"] = int(topic_bucket["total_records"]) + total_items
        topic_bucket["pending_records"] = int(topic_bucket["pending_records"]) + pending_items
        topic_bucket["resolved_records"] = int(topic_bucket["resolved_records"]) + resolved_items

    group_rows.sort(
        key=lambda row: (
            int(row.get("pending_records", 0) or 0),
            int(row.get("total_records", 0) or 0),
            str(row.get("pain_group_key", "") or ""),
        ),
        reverse=True,
    )
    topic_rows = sorted(
        topic_rollup.values(),
        key=lambda row: (
            int(row.get("pending_records", 0) or 0),
            int(row.get("total_records", 0) or 0),
            str(row.get("pain_topic", "") or ""),
        ),
        reverse=True,
    )
    focus_group = next(
        (row for row in group_rows if bool(row.get("is_focus_group", False))),
        {},
    )
    focus_removable = int(focus_group.get("removable_records_if_group_resolved", 0) or 0)
    elimination_ratio = round(
        float(focus_removable) / float(max(total_pending, 1)),
        4,
    ) if total_pending > 0 else 0.0

    return {
        "total_pain_group_types": len(group_rows),
        "total_pain_topic_types": len(topic_rows),
        "total_records": total_records,
        "pending_records": total_pending,
        "resolved_records": total_resolved,
        "focus_group_key": focus_group_key,
        "focus_group_removable_records_if_resolved": focus_removable,
        "focus_group_elimination_ratio_on_pending": elimination_ratio,
        "pain_groups_v1": group_rows,
        "pain_topics_v1": topic_rows,
    }


def _build_waiting_instruction(
    *,
    mode: str,
    focus_group_key: str,
    next_group_key: str,
    all_resolved: bool,
) -> dict[str, Any]:
    def _manual_repair_cmd(group_key: str) -> str:
        base = "$Meta-Runtime-Selfcheck 修复"
        key = str(group_key or "").strip()
        if key:
            base = f"{base} --group-key {key}"
        return (
            f'{base} --manual-repair-applied --manual-repair-path "<changed_path>" '
            '--verify-cmd "<verify_cmd>"'
        )

    focus_repair_cmd = _manual_repair_cmd(focus_group_key)
    next_repair_cmd = _manual_repair_cmd(next_group_key) if next_group_key else ""
    if all_resolved:
        message = "全部修复，没有其他痛点可修了。等待新的诊断指令。"
    elif mode == "repair":
        message = "修复执行已结束。请继续下达修复指令，或先执行诊断查看新的焦点痛点。"
    else:
        message = "完整痛点上下文报告已生成。请下达修复指令。"

    commands = [
        "$Meta-Runtime-Selfcheck >",
        focus_repair_cmd,
    ]
    if next_repair_cmd:
        commands.append(next_repair_cmd)

    return {
        "state": "awaiting_instruction",
        "message": message,
        "accepted_mode_tokens": [DIAGNOSE_TOKEN, REPAIR_TOKEN],
        "focus_group_key": focus_group_key,
        "next_group_key": next_group_key,
        "recommended_commands": [cmd for cmd in commands if cmd],
    }


def _build_report_only_output(
    *,
    status: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    groups = payload.get("groups", []) if isinstance(payload.get("groups", []), list) else []
    focus_group = payload.get("focus_group_v2", {}) if isinstance(payload.get("focus_group_v2", {}), dict) else {}
    focus_group_key = str(focus_group.get("pain_group_key", "") or "")
    selected_focus_group = next(
        (
            row
            for row in groups
            if isinstance(row, dict) and str(row.get("pain_group_key", "") or "") == focus_group_key
        ),
        {},
    )
    diagnosis_card = (
        selected_focus_group.get("diagnosis_card_v2", {})
        if isinstance(selected_focus_group.get("diagnosis_card_v2", {}), dict)
        else {}
    )
    repair_strategy = (
        diagnosis_card.get("repair_strategy_v2", {})
        if isinstance(diagnosis_card.get("repair_strategy_v2", {}), dict)
        else {}
    )
    meta_reasoningchain = (
        diagnosis_card.get("meta_reasoningchain_v1", {})
        if isinstance(diagnosis_card.get("meta_reasoningchain_v1", {}), dict)
        else {}
    )
    future_shape = (
        meta_reasoningchain.get("future_shape", {})
        if isinstance(meta_reasoningchain.get("future_shape", {}), dict)
        else {}
    )
    next_pain = payload.get("next_pain_v1", {}) if isinstance(payload.get("next_pain_v1", {}), dict) else {}
    next_group_key = str(next_pain.get("pain_group_key", "") or "")
    mode = str(payload.get("mode", "diagnose") or "diagnose")
    all_resolved = bool(payload.get("all_pain_resolved_v1", False))

    report_payload: dict[str, Any] = {
        "report_mode": "pain_context_report_only_v2",
        "research_scope_v1": {
            "data_source": "external pain provider optimization-list",
            "grouping_basis": "pain_group_key",
            "scope_policy": "all_threads",
            "evidence_sample_count": len(
                diagnosis_card.get("fact_evidence_samples", [])
                if isinstance(diagnosis_card.get("fact_evidence_samples", []), list)
                else []
            ),
        },
        "pain_inventory_v2": _build_pain_inventory(
            groups=groups,
            focus_group_key=focus_group_key,
        ),
        "focus_pain_context_v2": {
            "pain_group_key": focus_group_key,
            "pain_topic": str(selected_focus_group.get("pain_topic", "") or ""),
            "problem_statement": str(selected_focus_group.get("problem_statement", "") or ""),
            "focus_group_v2": focus_group,
            "full_group_context_v2": selected_focus_group,
            "diagnosis_card_v2": diagnosis_card,
            "repair_strategy_v2": repair_strategy,
            "meta_reasoningchain_v1": meta_reasoningchain,
            "before_after_shape_v1": future_shape,
        },
        "next_pain_context_v1": next_pain,
        "all_pain_resolved_v1": all_resolved,
    }

    if mode == "repair":
        report_payload["repair_runtime_v1"] = {
            "repair_execution_v1": payload.get("repair_execution_v1", {}),
            "repair_writeback_v1": payload.get("repair_writeback", {}),
            "post_repair_queue_summary": payload.get("post_repair_queue_summary", {}),
        }

    return {
        "status": status,
        "runtime_pain_batch_selfcheck_v1": {
            "run_id": str(payload.get("run_id", "") or ""),
            "mode": mode,
            "report_contract": "pain_context_report_only_v2",
            "pain_context_report_v2": report_payload,
            "waiting_instruction_v1": _build_waiting_instruction(
                mode=mode,
                focus_group_key=focus_group_key,
                next_group_key=next_group_key,
                all_resolved=all_resolved,
            ),
        },
    }
