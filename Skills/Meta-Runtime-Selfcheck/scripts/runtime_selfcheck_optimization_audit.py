from __future__ import annotations

import hashlib
import shlex

from runtime_pain_observability import normalize_text
from runtime_pain_types import OptimizationAudit
from runtime_pain_types import OptimizationOpportunity
from runtime_pain_types import TurnEvidence
from runtime_selfcheck_command_governance import normalize_command


def _command_tokens(command: str) -> list[str]:
    try:
        return list(shlex.split(str(command or "").strip()))
    except ValueError:
        return []


def _is_pre_exec_check(command: str) -> bool:
    text = str(command or "")
    return "Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py" in text and " pre-exec-check " in f" {text} "


def _is_governed_command(command: str) -> bool:
    text = str(command or "")
    tokens = _command_tokens(text)
    if not tokens:
        return False
    if _is_pre_exec_check(text):
        return False
    if len(tokens) > 2 and tokens[1] == "-m" and tokens[2] == "pytest":
        return True
    governed_markers = (
        "Skills/",
        "Cli_Toolbox.py",
        "run_python_code_lints.py",
        "Meta-github-operation",
        "git ",
    )
    return any(marker in text for marker in governed_markers)


def _is_help_command(command: str) -> bool:
    return "--help" in f" {str(command or '').strip()} "


def _opportunity_id(turn: TurnEvidence, kind: str, anchor: str) -> str:
    session_id = str(turn.get("session_id", "") or "")
    turn_id = str(turn.get("turn_id", "") or "")
    base = f"{session_id}|{turn_id}|{kind}|{anchor}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:24]


def _build_opportunity(
    turn: TurnEvidence,
    *,
    kind: str,
    optimization_level: str,
    priority: str,
    title: str,
    summary: str,
    evidence: list[str],
    current_approach: str,
    better_pattern: str,
    recommendation_class: str,
    suggested_action: str,
    recommendation_reason: str,
    expected_benefit: str,
    risk: str,
    comparison_baseline: str,
    anchor: str,
) -> OptimizationOpportunity:
    return {
        "optimization_id": _opportunity_id(turn, kind, anchor),
        "classification": "optimization_point",
        "kind": kind,
        "optimization_level": optimization_level,
        "priority": priority,
        "title": title,
        "summary": summary,
        "evidence": evidence,
        "current_approach": current_approach,
        "better_pattern": better_pattern,
        "equivalence_conditions": [
            "Target output or user-visible result is materially the same.",
            "Side-effect boundary stays inside the same governed scope.",
            "Risk boundary does not expand relative to the observed path.",
            "Observable verification or closure signal remains available.",
        ],
        "exclusion_conditions": [
            "Do not classify as optimization point when the alternative changes the required output, widens side effects, or raises unresolved risk.",
            "Do not classify as optimization point when the observed signal is already a real blocker, error, or explicitly whitelisted expected failure.",
        ],
        "why_not_problem": "The run completed without a blocking failure on this path, so immediate repair is unnecessary.",
        "why_not_expected_failure": "This is not an intentionally whitelisted red signal; it is a successful or acceptable path that is still suboptimal.",
        "knowledge_comparison_basis": "The recommendation is based on a concrete comparison between the observed path and a better known governed pattern the model can already articulate and justify.",
        "recommendation_class": recommendation_class,
        "suggested_action": suggested_action,
        "recommendation_reason": recommendation_reason,
        "expected_benefit": expected_benefit,
        "risk": risk,
        "comparison_baseline": comparison_baseline,
        "should_recommend_execution": True,
    }


def build_turn_optimization_audit(
    *,
    turn: TurnEvidence,
    issue_items: list[dict[str, object]] | None = None,
) -> OptimizationAudit:
    if str(turn.get("status", "") or "") != "completed":
        return {
            "status": "deferred_until_turn_end",
            "opportunity_count": 0,
            "recommendation_buckets": {},
            "optimization_level_buckets": {},
            "opportunities": [],
            "summary": "Turn is still active; optimization audit is deferred until turn end so it can evaluate the whole execution path.",
        }

    opportunities: list[OptimizationOpportunity] = []
    tool_events = [event for event in list(turn.get("tool_events", [])) if isinstance(event, dict)]
    issue_signatures = {
        str(item.get("source_event", {}).get("command_signature", "") or "")
        for item in issue_items or []
        if isinstance(item, dict)
    }

    governed_success_without_preexec: list[str] = []
    seen_preexec = False
    for event in tool_events:
        command = str(event.get("command_preview", "") or "")
        if _is_pre_exec_check(command):
            seen_preexec = True
            continue
        if str(event.get("status", "") or "") != "ok":
            continue
        if not _is_governed_command(command):
            continue
        if str(event.get("command_signature", "") or "") in issue_signatures:
            continue
        if not seen_preexec:
            governed_success_without_preexec.append(command)
    if governed_success_without_preexec:
        evidence = [normalize_text(item, limit=180) for item in governed_success_without_preexec[:3]]
        opportunities.append(
            _build_opportunity(
                turn,
                kind="missing_pre_exec_governance",
                optimization_level="method",
                priority="p2",
                title="Governed commands ran without pre-exec adjudication",
                summary="本轮存在成功执行的受管命令，但没有先走 pre-exec-check，说明运行流程仍未收敛到最优 canonical path。",
                evidence=evidence,
                current_approach="Run governed commands directly and rely on success without first-class pre-exec normalization.",
                better_pattern="Classify governed commands through pre-exec-check before execution and then run the normalized canonical path.",
                recommendation_class="optimize_runflow",
                suggested_action="在 repo-local Python、lint、traceability、git 与 skill CLI 前统一插入 pre-exec-check。",
                recommendation_reason="Missing pre-exec does not always fail immediately, but it leaves preventable drift, cost, and first-failure risk in the flow.",
                expected_benefit="Lower first-pass failure rate and more stable governed execution.",
                risk="Slightly more command overhead per governed action.",
                comparison_baseline="Known better practice is to classify governed commands before execution, not after the first avoidable deviation.",
                anchor="missing_pre_exec_governance",
            )
        )

    for event in tool_events:
        if str(event.get("status", "") or "") != "ok":
            continue
        command = str(event.get("command_preview", "") or "")
        if str(event.get("command_signature", "") or "") in issue_signatures:
            continue
        normalized = normalize_command(command, workdir=str(turn.get("cwd", "") or ""))
        if not bool(normalized.get("changed", False)):
            continue
        repair_types = list(normalized.get("repair_types", []))
        evidence = [normalize_text(command, limit=180)]
        opportunities.append(
            _build_opportunity(
                turn,
                kind="noncanonical_but_successful_command",
                optimization_level="code",
                priority="p2",
                title="A successful command still deviated from the canonical governed surface",
                summary=f"命令虽然成功，但若预先归一化仍会被改写为更优 canonical 形态：{', '.join(repair_types) or 'governed normalization'}。",
                evidence=evidence,
                current_approach="Keep a looser successful command shape that still reaches the target outcome.",
                better_pattern="Use the already-known normalized command shape as the single canonical entrypoint.",
                recommendation_class="optimize_runflow",
                suggested_action="把该类命令直接收敛到 governed canonical entrypoint，而不是依赖运行后偶然成功。",
                recommendation_reason="A noncanonical success is still a process optimization signal because it relies on a looser path than the governed contract prefers.",
                expected_benefit="Reduced drift between actual execution and the documented best path.",
                risk="Low; this mostly standardizes entrypoints rather than changing behavior.",
                comparison_baseline="Known better practice is to execute the already-normalized command directly.",
                anchor=str(event.get("command_signature", "") or command),
            )
        )

    help_commands = [
        str(event.get("command_preview", "") or "")
        for event in tool_events
        if str(event.get("status", "") or "") == "ok" and _is_help_command(str(event.get("command_preview", "") or ""))
    ]
    if len(help_commands) >= 2:
        opportunities.append(
            _build_opportunity(
                turn,
                kind="surface_discoverability_gap",
                optimization_level="skill",
                priority="p3",
                title="The run spent multiple command rounds discovering the interface surface",
                summary=f"本轮出现 {len(help_commands)} 次 `--help` / surface discovery 调用，说明合同或门面还不够直达。",
                evidence=[normalize_text(item, limit=160) for item in help_commands[:3]],
                current_approach="Require repeated surface discovery before the canonical path becomes obvious.",
                better_pattern="Expose the canonical entrypoint, arguments, and closeout path directly in the skill facade and runtime contract.",
                recommendation_class="upgrade_skill",
                suggested_action="强化相关技能门面与 runtime contract，让 canonical entrypoint、常用参数与 closeout 路径更早可见。",
                recommendation_reason="Multiple help rounds are not failures, but they indicate avoidable discovery cost and weak interface affordance.",
                expected_benefit="Lower token, latency, and cognitive cost before the first successful action.",
                risk="Low; document and facade tightening only.",
                comparison_baseline="Known better practice is to expose the canonical path clearly enough that repeated help lookups are unnecessary.",
                anchor="surface_discoverability_gap",
            )
        )

    total_commands = len(tool_events)
    if total_commands >= 8 and not issue_items:
        opportunities.append(
            _build_opportunity(
                turn,
                kind="execution_cost_above_baseline",
                optimization_level="task",
                priority="p3",
                title="The turn completed, but the execution path was longer than the governed baseline",
                summary=f"本轮共有 {total_commands} 次工具执行，虽然没有问题项，但执行成本已明显高于轻量闭环的目标形态。",
                evidence=[f"total_tool_events={total_commands}"],
                current_approach="Complete the task through a longer multi-step route that still reaches the intended result.",
                better_pattern="Choose a shorter task-level route that preserves the same result, guard rails, and closure evidence with fewer intermediate actions.",
                recommendation_class="suggestion_only",
                suggested_action="审计是否可以减少无增益检查、重复读取或中间探测，并把高频步骤收敛到更短的 canonical path。",
                recommendation_reason="A successful but overlong path is an optimization signal when it adds cost without adding confidence.",
                expected_benefit="Lower latency and lower operational overhead on future turns.",
                risk="Medium; aggressive shortening can remove useful guard rails if applied without judgment.",
                comparison_baseline="Known better practice is to keep a smooth governed turn compact once the canonical route is already known.",
                anchor="execution_cost_above_baseline",
            )
        )

    deduped: dict[str, OptimizationOpportunity] = {}
    for row in opportunities:
        deduped[str(row.get("optimization_id", "") or "")] = row
    ordered = sorted(
        deduped.values(),
        key=lambda row: (
            {"p0": 3, "p1": 2, "p2": 1, "p3": 0}.get(str(row.get("priority", "") or ""), 0),
            str(row.get("title", "") or ""),
        ),
        reverse=True,
    )
    recommendation_buckets: dict[str, int] = {}
    optimization_level_buckets: dict[str, int] = {}
    for row in ordered:
        bucket = str(row.get("recommendation_class", "") or "")
        recommendation_buckets[bucket] = recommendation_buckets.get(bucket, 0) + 1
        level = str(row.get("optimization_level", "") or "")
        optimization_level_buckets[level] = optimization_level_buckets.get(level, 0) + 1

    summary = (
        "No optimization opportunities were detected beyond the problem/expected-failure track."
        if not ordered
        else (
            f"Detected {len(ordered)} optimization opportunities after the run completed; "
            "each item preserves the same target outcome and risk boundary while comparing the observed path against a better known pattern."
        )
    )
    return {
        "status": "completed",
        "opportunity_count": len(ordered),
        "recommendation_buckets": recommendation_buckets,
        "optimization_level_buckets": optimization_level_buckets,
        "opportunities": ordered,
        "summary": summary,
    }
