from __future__ import annotations

from typing import Any

_ACTIVITY_RULES = (
    ("governance_gate.py", "当时在执行治理门禁检查，目的是验证本轮改动是否可放行。"),
    ("l2_structure_lint.py", "当时在执行结构一致性检查，目的是确认结构层级和索引完整。"),
    ("runtime_pain_batch.py", "当时在执行痛点聚类自检，目的是沉淀可修复的问题组。"),
    ("optimization-resolve", "当时在回写修复状态，目的是清理已闭环痛点。"),
)

_EXPECTED_RULES = (
    ("--mode gate", "预期结果是 gate 返回 PASS 且 exit code 为 0。"),
    ("lint", "预期结果是 lint 通过且没有阻断错误。"),
    ("--test-root", "预期结果是目标目录检查通过并产出可用结果。"),
)


def _pick_text(values: list[Any]) -> str:
    return next((str(v).strip() for v in values if str(v).strip()), "")


def _activity_from_command(command_preview: str) -> str:
    lowered = str(command_preview or "").lower()
    matched = next((desc for key, desc in _ACTIVITY_RULES if key in lowered), "")
    return matched or "当时在执行运行时命令，希望推进当前任务到下一个可验证阶段。"


def _expected_from_command(command_preview: str) -> str:
    lowered = str(command_preview or "").lower()
    matched = next((desc for key, desc in _EXPECTED_RULES if key in lowered), "")
    return matched or "预期结果是命令成功执行（exit code=0），并进入下一步。"


def _root_cause_hypotheses(
    *,
    kinds: set[str],
    trigger_nodes: list[str],
    trigger_scripts: list[str],
    pending_items: int,
    total_items: int,
) -> list[dict[str, str]]:
    hypotheses: list[dict[str, str]] = []
    kind_hypotheses = {
        "trial_and_error_loop": (
            "同一节点缺少决策阈值与退出条件，导致反复试错。",
            "high",
            "kind 命中 trial_and_error_loop。",
        ),
        "tool_failure_any": (
            "失败分支和预检缺失，异常后仍走原路径重复触发。",
            "high",
            "kind 命中 tool_failure_any。",
        ),
        "phase_incomplete": (
            "阶段门禁/验收条件不完整，导致半完成状态被重复记录。",
            "medium",
            "kind 命中 phase_incomplete。",
        ),
    }
    for key, (hypothesis, confidence, evidence_basis) in kind_hypotheses.items():
        if key in kinds:
            hypotheses.append(
                {
                    "hypothesis": hypothesis,
                    "confidence": confidence,
                    "evidence_basis": evidence_basis,
                }
            )

    if len(trigger_nodes) == 1 and pending_items >= 2:
        hypotheses.append(
            {
                "hypothesis": "痛点高度集中在单节点，局部修复可显著降低重复记录。",
                "confidence": "medium",
                "evidence_basis": f"触发节点唯一且 pending={pending_items}。",
            }
        )
    if len(trigger_scripts) == 1 and total_items >= 3:
        hypotheses.append(
            {
                "hypothesis": "触发脚本稳定重复，在该脚本补齐兜底分支和终止条件会直接降低复发率。",
                "confidence": "medium",
                "evidence_basis": f"触发脚本唯一且 total={total_items}。",
            }
        )
    if not hypotheses:
        hypotheses.append(
            {
                "hypothesis": "节点稳定化策略不足（预检/失败处理/回退）导致重复痛点堆积。",
                "confidence": "low",
                "evidence_basis": "未命中特定 kind，使用通用稳定性推断。",
            }
        )
    return hypotheses[:4]


def _action_plan(
    *,
    remediation_action: str,
    kinds: set[str],
    trigger_nodes: list[str],
    trigger_scripts: list[str],
) -> list[dict[str, Any]]:
    node_hint = trigger_nodes[0] if trigger_nodes else "目标触发节点"
    script_hint = trigger_scripts[0] if trigger_scripts else "目标触发脚本"
    guard_step = "在触发前增加输入校验与环境预检，失败立即分流"
    guard_step_by_kind = {
        "trial_and_error_loop": "加入重试上限、超时与停止条件，避免同路径反复试错",
        "phase_incomplete": "补齐阶段完成门禁，未满足验收则禁止流转下一阶段",
    }
    guard_override = next((step for key, step in guard_step_by_kind.items() if key in kinds), "")
    guard_step = guard_override or guard_step

    return [
        {
            "phase": "immediate",
            "objective": "止血并阻断重复写入",
            "steps": [
                f"优先处理节点 `{node_hint}` 与脚本 `{script_hint}`。",
                guard_step,
                "新增失败回退路径，确保异常后进入可执行下一步。",
            ],
        },
        {
            "phase": "short_term",
            "objective": "将修复显式写回 memory",
            "steps": [
                remediation_action,
                "按 pain_group_key 批量执行 resolve，避免逐条手工处理。",
                "下一轮仅聚焦未修复 pending 组，持续清理存量痛点。",
            ],
        },
        {
            "phase": "hardening",
            "objective": "降低复发率",
            "steps": [
                "为同类节点建立统一的预检/重试/回退模板。",
                "在记录阶段保留一致性键（pain_group_key / consistency_hash）用于去重与归并。",
            ],
        },
    ]


def _acceptance_checks(
    *,
    pain_group_key: str,
    pending_items: int,
    trigger_nodes: list[str],
    trigger_scripts: list[str],
) -> list[str]:
    node_hint = trigger_nodes[0] if trigger_nodes else "目标节点"
    script_hint = trigger_scripts[0] if trigger_scripts else "目标脚本"
    return [
        f"{pain_group_key} 在下一轮自检中 pending_items 低于当前值 {pending_items}。",
        f"`{node_hint}` 触发失败时可观察到明确回退/分流记录。",
        f"`{script_hint}` 在连续两轮中不再新增同组痛点。",
        "repair_mode 写回后，post_repair_queue_summary 的 pending_items 持续下降。",
    ]


def _infer_change_operation(step_title: str, instruction: str) -> str:
    text = f"{step_title} {instruction}"
    if any(token in text for token in ("新增", "加入", "补齐")):
        return "add"
    if any(token in text for token in ("改为", "重写", "替换")):
        return "replace"
    return "update"


def _build_routing_table(
    *,
    strategy_key: str,
    node_hint: str,
    script_hint: str,
    pain_group_key: str,
) -> list[dict[str, Any]]:
    base = [
        {
            "route_id": "R1_PRECHECK_BLOCK",
            "trigger_condition": "preflight(ctx).ok == false",
            "decision": f"停止 `{script_hint}` 在 `{node_hint}` 的主执行路径，直接输出 reason_code 并写入 blocker。",
            "next_state": "blocked_for_fix",
        },
        {
            "route_id": "R2_RECOVERABLE_RETRY_ONCE",
            "trigger_condition": "error.class in recoverable and retry_count < 1",
            "decision": "允许 1 次受控重试；重试后仍失败则转入 fallback。",
            "next_state": "retry_once_then_fallback",
        },
        {
            "route_id": "R3_NONRECOVERABLE_FALLBACK",
            "trigger_condition": "error.class in non_recoverable",
            "decision": "直接进入 fallback handler，禁止沿原路径继续重试。",
            "next_state": "fallback_handled",
        },
        {
            "route_id": "R4_UNKNOWN_SAFE_STOP",
            "trigger_condition": "error.class == unknown",
            "decision": f"立即安全停止并保留 `{pain_group_key}` 的 pending，等待机制修复后再执行。",
            "next_state": "safe_stop_pending",
        },
    ]
    if strategy_key == "phase_incomplete":
        base[0]["trigger_condition"] = "phase_input_complete == false"
        base[0]["decision"] = f"在 `{node_hint}` 阶段入口直接阻断并返回缺口清单。"
    if strategy_key == "trial_and_error_loop":
        base[1]["trigger_condition"] = "should_retry(error, context) == true and retry_count < 1"
    return base


def _build_resolve_guard(
    *,
    pain_group_key: str,
) -> dict[str, Any]:
    return {
        "guard_state": "active",
        "guard_goal": "prevent_cover_up",
        "must_have_evidence_v1": [
            "adjudicated_directives_applied == true",
            "verification_runbook_passed == true",
            "next_diagnose_same_group_pending_decreased == true",
        ],
        "deny_if_v1": [
            "only_memory_resolve_written_without_runtime_evidence == true",
            "verification_not_executed == true",
            "next_diagnose_same_group_new_pain_added == true",
        ],
        "repair_mode_behavior": (
            f"仅当 must_have 全部满足且 deny_if 全部不命中时，`{pain_group_key}` 才允许写入 resolved；"
            "否则保持 pending。"
        ),
        "deny_result_state": "pending",
    }


def _directive_before_state(directive: dict[str, Any]) -> str:
    operation = str(directive.get("operation", "") or "")
    if operation == "add":
        return "当前路径缺少该门禁/步骤，失败场景会直接进入主执行或无保护重试。"
    if operation == "replace":
        return "当前失败分支仍沿旧路径执行，未形成明确分流与兜底。"
    if operation == "update":
        return "当前策略阈值不稳定或未固化，导致重复失败概率偏高。"
    if operation == "remove":
        return "当前存在冗余/冲突步骤，放大了误触发与歧义处理。"
    return "当前执行路径与目标治理路径不一致。"


def _build_change_manifest(
    *,
    directives: list[dict[str, Any]],
    pain_group_key: str,
) -> dict[str, Any]:
    buckets: dict[str, list[dict[str, Any]]] = {"add": [], "modify": [], "remove": []}
    for directive in directives:
        if not isinstance(directive, dict):
            continue
        operation = str(directive.get("operation", "") or "")
        action = {"add": "add", "replace": "modify", "update": "modify", "remove": "remove"}.get(operation, "modify")
        target_location = directive.get("target_location", {}) if isinstance(directive.get("target_location", {}), dict) else {}
        buckets[action].append(
            {
                "directive_id": str(directive.get("directive_id", "") or ""),
                "target": {
                    "pain_group_key": str(target_location.get("pain_group_key", "") or pain_group_key),
                    "trigger_node": str(target_location.get("trigger_node", "") or ""),
                    "trigger_script": str(target_location.get("trigger_script", "") or ""),
                },
                "before": _directive_before_state(directive),
                "after": str(directive.get("decision", "") or ""),
                "reason": str(directive.get("definition_of_done", "") or ""),
            }
        )
    return {
        "add": buckets["add"],
        "modify": buckets["modify"],
        "remove": buckets["remove"],
        "summary": {
            "add_count": len(buckets["add"]),
            "modify_count": len(buckets["modify"]),
            "remove_count": len(buckets["remove"]),
        },
    }


def _build_meta_reasoningchain_contract(
    *,
    pain_group_key: str,
    pain_topic: str,
    pending_items: int,
    total_items: int,
    priority_top: str,
    manager_story_v1: dict[str, Any],
    repair_strategy_v2: dict[str, Any],
) -> dict[str, Any]:
    directives = repair_strategy_v2.get("adjudicated_directives_v1", [])
    directives = directives if isinstance(directives, list) else []
    routing_table = repair_strategy_v2.get("routing_table_v1", [])
    routing_table = routing_table if isinstance(routing_table, list) else []
    resolve_guard = repair_strategy_v2.get("resolve_guard_v1", {})
    resolve_guard = resolve_guard if isinstance(resolve_guard, dict) else {}
    change_manifest = _build_change_manifest(directives=directives, pain_group_key=pain_group_key)
    first_expected_after = ""
    expected_results = repair_strategy_v2.get("expected_results_v1", [])
    if isinstance(expected_results, list):
        first_expected_after = next((str(row) for row in expected_results if str(row).strip()), "")

    return {
        "current_hypothesis": {
            "statement": "同组失败在同节点重复出现，根因是缺少门禁与失败分流机制，导致盲重试放大痛点。",
            "confidence": "high",
            "evidence_scope": {
                "pain_group_key": pain_group_key,
                "pain_topic": pain_topic,
                "pending_items": pending_items,
                "total_items": total_items,
                "priority_top": priority_top,
            },
        },
        "future_shape": {
            "before_state_v1": {
                "what_we_were_doing": str(manager_story_v1.get("what_we_were_doing", "") or ""),
                "tool_execution": str(manager_story_v1.get("tool_execution", "") or ""),
                "expected_result": str(manager_story_v1.get("expected_result", "") or ""),
                "actual_result": str(manager_story_v1.get("actual_result", "") or ""),
                "why_this_created_hesitation": str(manager_story_v1.get("why_this_created_hesitation", "") or ""),
            },
            "after_state_target_v1": {
                "execution_shape": "preflight -> classify_error -> retry_once_or_fallback -> safe_stop_or_exit",
                "routing_contract": "按 routing_table_v1 执行分流，禁止默认盲重试。",
                "resolve_contract": "未满足 resolve_guard_v1 的 must_have 证据时，状态保持 pending。",
                "expected_result_after_fix": first_expected_after,
            },
            "change_manifest_v1": change_manifest,
        },
        "prompt_instruction_delta": {
            "new_required_sections": [
                "before_state_v1",
                "after_state_target_v1",
                "change_manifest_v1",
                "routing_table_v1",
                "resolve_guard_v1",
            ],
            "language_constraint": "裁决字段禁止建议语气（应该/建议/可考虑）。",
        },
        "model_behavior_delta": {
            "benefits": [
                "报告从建议说明升级为可执行裁决合同。",
                "管理者可直接判断分流路径与修复代价。",
                "通过 resolve_guard 降低“仅改状态”的遮盖风险。",
            ],
            "side_effects": [
                "输出篇幅增加。",
                "生成与校验成本上升。",
            ],
            "measurable_signals": [
                "mandatory_section_coverage == 100%",
                "advice_tone_hits_in_adjudicated_fields == 0",
                "routing_rule_count >= 3",
            ],
        },
        "tooling_lint_workflow_delta": {
            "tooling_changes": [
                "runtime_pain_narrative.py: 新增 Meta-reasoningchain 合同结构生成。",
                "runtime_pain_batch.py: focus_group 输出 before/after/change_manifest 摘要。",
                "SKILL.md: 输出合同升级为 reasoningchain 强制字段。",
            ],
            "workflow_changes": [
                "diagnose 输出裁决合同，不直接改业务代码。",
                "repair 写回前必须满足 resolve_guard_v1。",
            ],
        },
        "failure_modes_rollback_triggers": [
            {
                "failure_mode": "缺失 reasoningchain 强制段落。",
                "rollback_trigger": "missing_reasoning_sections_count > 0",
                "rollback_action": "回滚到上一版输出模板并阻断放行。",
            },
            {
                "failure_mode": "裁决字段出现建议语气。",
                "rollback_trigger": "advice_tone_hits_in_adjudicated_fields > 0",
                "rollback_action": "回滚并重生成裁决语句。",
            },
            {
                "failure_mode": "未满足证据仍写 resolved。",
                "rollback_trigger": "resolve_without_must_have_evidence_count >= 1",
                "rollback_action": "撤销 resolved 并恢复 pending。",
            },
        ],
        "minimum_pilot": {
            "scope": "focus_group 单组验证",
            "steps": [
                "只对排序第一痛点组生成完整 reasoningchain 合同。",
                "校验 change_manifest_v1 的 add/modify/remove 结构。",
                "复跑 diagnose 检查字段覆盖与语气约束。",
            ],
            "success_criteria": [
                "routing_table_v1 与 resolve_guard_v1 均非空。",
                "change_manifest_v1.summary.add_count + modify_count >= 2。",
                "advice_tone_hits_in_adjudicated_fields == 0。",
            ],
        },
        "decision_recommendation": {
            "decision": "go_with_guard",
            "rationale": "当前痛点具备明确分流路径与回滚阈值，可进入低风险试点强化。",
            "unknowns": [
                "实际工程代码路径是否与审计分流路径一一映射。",
            ],
        },
    }


def _build_repair_strategy(
    *,
    kinds: set[str],
    pain_group_key: str,
    pending_items: int,
    priority_top: str,
    trigger_nodes: list[str],
    trigger_scripts: list[str],
    command_preview: str,
) -> dict[str, Any]:
    node_hint = trigger_nodes[0] if trigger_nodes else "目标触发节点"
    script_hint = trigger_scripts[0] if trigger_scripts else "目标触发脚本"
    strategy_key = next(
        (key for key in ("tool_failure_any", "trial_and_error_loop", "phase_incomplete") if key in kinds),
        "default",
    )
    strategy_catalog: dict[str, dict[str, Any]] = {
        "tool_failure_any": {
            "repair_objective": "把“失败后重复触发”改成“失败后可判定分流”。",
            "changes": [
                (
                    "加 preflight 前置门禁",
                    f"在 `{node_hint}` 前新增 `preflight(ctx)->(ok, reason_code)`，不满足条件直接返回并记录 reason_code。",
                    "同类输入命中 preflight 失败时，不再进入主执行路径。",
                ),
                (
                    "重写失败分支",
                    "失败后统一写入 failure_class 并走 fallback handler，禁止沿原路径盲重试。",
                    "失败事件可区分“可恢复/不可恢复”，并有明确下一步动作。",
                ),
                (
                    "设置重试预算",
                    "仅对可恢复错误允许最多 1 次重试，超预算立刻中止并输出固定处置结论。",
                    "同组重复失败显著下降，下一轮 pending 明显减少。",
                ),
            ],
        },
        "trial_and_error_loop": {
            "repair_objective": "把“反复试错”改成“有停止条件的决策流程”。",
            "changes": [
                (
                    "定义决策阈值",
                    f"在 `{script_hint}` 路径新增 `should_retry(error, context)`，只有满足白名单条件才允许继续。",
                    "同类异常不再无限试错，出现不可恢复错误时立即停机分流。",
                ),
                (
                    "增加终止条件",
                    "加入 `max_attempts`、超时和重复签名熔断条件。",
                    "日志可见“为什么停止”，团队不再凭经验猜下一步。",
                ),
                (
                    "把经验固化为规则",
                    "将成功/失败判定沉淀到统一策略函数，后续同类节点复用。",
                    "同类任务决策一致，减少不同人处理方式漂移。",
                ),
            ],
        },
        "phase_incomplete": {
            "repair_objective": "把“阶段半完成”改成“门禁驱动的完整阶段收敛”。",
            "changes": [
                (
                    "补齐阶段入口门禁",
                    f"在 `{node_hint}` 前校验上游产物完整性，不满足直接阻断并提示缺口。",
                    "阶段不会在缺关键输入时继续推进。",
                ),
                (
                    "补齐阶段出口验收",
                    "定义阶段完成条件并落盘验收结果，未通过则禁止流入下阶段。",
                    "每次阶段结束都有明确 PASS/FAIL 与缺口项。",
                ),
                (
                    "失败后回退到可执行状态",
                    "为每个阶段定义回退动作，避免卡在中间态。",
                    "阶段失败后团队知道“现在该做什么”，不再等待拍板。",
                ),
            ],
        },
        "default": {
            "repair_objective": "把“重复痛点记录”改成“稳定可预测的执行路径”。",
            "changes": [
                (
                    "增加前置校验",
                    f"在 `{node_hint}` 前增加输入与环境检查，不满足时直接分流。",
                    "坏输入不会进入主流程。",
                ),
                (
                    "定义失败处理标准动作",
                    "失败后写入统一分类和下一步动作，避免人工临场判断。",
                    "失败后的动作可重复、可追踪。",
                ),
                (
                    "定义验收阈值",
                    f"把 `{pain_group_key}` 的 pending 下降设为必达指标。",
                    "修复完成有客观标准，而不是主观感觉。",
                ),
            ],
        },
    }
    strategy = strategy_catalog[strategy_key]
    how_to_fix = [
        {
            "step": idx,
            "what_to_change": change[0],
            "how_to_implement": change[1],
            "definition_of_done": change[2],
        }
        for idx, change in enumerate(strategy["changes"], start=1)
    ]
    adjudicated_directives_v1 = [
        {
            "directive_id": f"D{idx}",
            "decision": change[1],
            "operation": _infer_change_operation(change[0], change[1]),
            "target_location": {
                "trigger_node": node_hint,
                "trigger_script": script_hint,
                "pain_group_key": pain_group_key,
            },
            "definition_of_done": change[2],
        }
        for idx, change in enumerate(strategy["changes"], start=1)
    ]
    target_state_v1 = [
        f"`{node_hint}` 的失败路径具备 preflight + fallback + 重试预算三件套。",
        f"`{script_hint}` 触发失败时会输出可判定的 reason_code/failure_class。",
        f"`{pain_group_key}` 不再持续堆积重复 pending。",
    ]
    expected_results_v1 = [
        "同类任务从“随机重试”变成“可预测收敛”，处理节奏稳定。",
        f"下一轮自检中该组 pending 少于当前值 {pending_items}。",
        "团队在失败发生后能立即判断是“继续、回退、还是停止修机制”。",
    ]
    verification_runbook_v1 = [
        {
            "check": "重放当前关键命令并观察执行路径",
            "command_hint": command_preview or "复用当前组命令签名重跑一次",
            "expected_signal": "失败时出现明确分流/停止原因，不再无条件重复触发。",
        },
        {
            "check": "重新执行 selfcheck >",
            "command_hint": "python3 .../runtime_pain_batch.py \">\" --session-scope-mode all_threads",
            "expected_signal": f"{pain_group_key} 的 pending 数下降。",
        },
        {
            "check": "执行 修复 回写并复检",
            "command_hint": f"python3 .../runtime_pain_batch.py 修复 --group-key {pain_group_key}",
            "expected_signal": "post_repair_queue_summary.pending_items 持续下降。",
        },
    ]
    routing_table_v1 = _build_routing_table(
        strategy_key=strategy_key,
        node_hint=node_hint,
        script_hint=script_hint,
        pain_group_key=pain_group_key,
    )
    resolve_guard_v1 = _build_resolve_guard(pain_group_key=pain_group_key)
    return {
        "decision_state": "adjudicated",
        "decision_basis": "pain_group_key + trigger_node + trigger_script + kind",
        "repair_objective": strategy["repair_objective"],
        "adjudicated_directives_v1": adjudicated_directives_v1,
        "routing_table_v1": routing_table_v1,
        "resolve_guard_v1": resolve_guard_v1,
        "how_to_fix_v1": how_to_fix,
        "target_state_v1": target_state_v1,
        "expected_results_v1": expected_results_v1,
        "verification_runbook_v1": verification_runbook_v1,
    }


def build_narrative_package(
    *,
    pain_group_key: str,
    pain_topic: str,
    kinds: set[str],
    trigger_nodes: list[str],
    trigger_scripts: list[str],
    pending_items: int,
    total_items: int,
    priority_top: str,
    remediation_action: str,
    events_sorted: list[dict[str, Any]],
) -> dict[str, Any]:
    first = events_sorted[0] if events_sorted else {}
    command_preview = _pick_text([first.get("command_preview", ""), first.get("command_signature", "")])
    actual_result = _pick_text([first.get("outcome", ""), first.get("summary", ""), first.get("title", "")])
    tool_name = _pick_text([first.get("tool_name", ""), "unknown_tool"])
    why = _pick_text([first.get("why", ""), "runtime_tool_failure"])

    root_cause_hypotheses = _root_cause_hypotheses(
        kinds=kinds,
        trigger_nodes=trigger_nodes,
        trigger_scripts=trigger_scripts,
        pending_items=pending_items,
        total_items=total_items,
    )
    action_plan_v1 = _action_plan(
        remediation_action=remediation_action,
        kinds=kinds,
        trigger_nodes=trigger_nodes,
        trigger_scripts=trigger_scripts,
    )
    acceptance_checks_v1 = _acceptance_checks(
        pain_group_key=pain_group_key,
        pending_items=pending_items,
        trigger_nodes=trigger_nodes,
        trigger_scripts=trigger_scripts,
    )
    repair_strategy_v2 = _build_repair_strategy(
        kinds=kinds,
        pain_group_key=pain_group_key,
        pending_items=pending_items,
        priority_top=priority_top,
        trigger_nodes=trigger_nodes,
        trigger_scripts=trigger_scripts,
        command_preview=command_preview,
    )
    objective = _pick_text([repair_strategy_v2.get("repair_objective", "")])
    expected_after_fix = repair_strategy_v2.get("expected_results_v1", [])
    if not isinstance(expected_after_fix, list):
        expected_after_fix = []

    hesitation_reason = (
        "同一类失败在同节点反复出现但没有稳定分流策略，团队会在“继续重试”与“停下来修机制”之间反复摇摆。"
        if pending_items >= 2
        else "当前失败尚未形成大规模重复，但若不补预检与回退，容易扩散成持续犹豫。"
    )
    manager_story_v1 = {
        "what_we_were_doing": _activity_from_command(command_preview),
        "tool_execution": f"使用工具 `{tool_name}` 执行命令：{command_preview or '命令内容缺失'}",
        "expected_result": _expected_from_command(command_preview),
        "actual_result": actual_result or "实际结果字段缺失，需补齐 outcome/summary。",
        "why_this_created_hesitation": hesitation_reason,
        "strengthening_plan": (
            f"已裁决执行：{objective or '围绕该组补齐预检、失败分流和验收门禁。'} "
            f"围绕组 `{pain_group_key}`（{pain_topic}）按修复蓝图逐项落地。"
        ),
        "expected_after_fix": expected_after_fix[:3],
        "executive_summary": (
            f"这是一个 {pending_items}/{total_items} 的重复失败组（原因标签：{why}），"
            "已裁决按单组治理并批量回写。"
        ),
    }
    meta_reasoningchain_v1 = _build_meta_reasoningchain_contract(
        pain_group_key=pain_group_key,
        pain_topic=pain_topic,
        pending_items=pending_items,
        total_items=total_items,
        priority_top=priority_top,
        manager_story_v1=manager_story_v1,
        repair_strategy_v2=repair_strategy_v2,
    )

    return {
        "root_cause_hypotheses": root_cause_hypotheses,
        "action_plan_v1": action_plan_v1,
        "acceptance_checks_v1": acceptance_checks_v1,
        "repair_strategy_v2": repair_strategy_v2,
        "manager_story_v1": manager_story_v1,
        "meta_reasoningchain_v1": meta_reasoningchain_v1,
    }
