#!/usr/bin/env python3
"""Contracts/constants for MSTG L0-L13 writeback and anchor mapping."""

from __future__ import annotations

BASELINE_CHAIN_PACKETS: dict[str, list[str]] = {
    "chain_tool_inventory_baseline": [
        "m1_collect_tool_registry_snapshot",
        "m2_scan_target_entrypoints",
        "m3_tool_domain_owner_classification",
        "m4_anchor_binding_baseline",
        "m5_inventory_acceptance",
    ],
    "chain_usage_contract_backfill": [
        "m1_usage_command_examples",
        "m2_usage_inputs_outputs",
        "m3_usage_doc_anchor_binding",
        "m4_usage_nonempty_validation",
        "m5_usage_contract_gate",
    ],
    "chain_modification_development_backfill": [
        "m1_modification_workflow_contract",
        "m2_required_docs_matrix",
        "m3_sync_contract_and_guardrails",
        "m4_development_record_policy",
        "m5_modification_development_gate",
    ],
    "chain_sync_traceability_closure": [
        "m1_registry_docs_sync_check",
        "m2_machine_map_anchor_sync",
        "m3_change_ledger_traceability",
        "m4_gate_and_outcome_lint",
        "m5_l13_closure_archive",
    ],
    "chain_batch_governance_rollout": [
        "m1_target_discovery",
        "m2_batch_tool_inventory_alignment",
        "m3_batch_tool_doc_backfill",
        "m4_scope_whitelist_and_audit_sync",
    ],
}

CHAIN_OBJECTIVES: dict[str, str] = {
    "chain_tool_inventory_baseline": "先把目标技能现有工具做完整盘点（tool_id/entrypoint/domain/owner），建立文档回填索引基线。",
    "chain_usage_contract_backfill": "为每个工具补齐可执行的使用文档（命令示例、输入输出、锚点映射），让接手者可直接运行。",
    "chain_modification_development_backfill": "为每个工具补齐修改与开发文档（更新流程、必更文档、开发留痕），降低后续改造摩擦。",
    "chain_sync_traceability_closure": "确保 registry/docs/machine-map/ledger 同步并通过 gate/outcome lint，形成可审计闭环。",
    "chain_batch_governance_rollout": "批量治理多个技能时复用同一套工具文档回填流程，并同步白名单与审计轨迹。",
}

STATIC_LAYER_SECTIONS: dict[int, dict[str, list[str]]] = {
    3: {
        "## 共享运行时与依赖策略": [
            "工具文档脚本与业务脚本分层维护，防止职责串线",
            "依赖优先复用成熟组件，禁止为文档写回重复造轮子",
            "共享虚拟环境路径固定且可复用，确保工具文档脚本可重复执行",
        ]
    },
    4: {
        "## 决策与控制点": [
            "文档写回脚本默认无 secret 依赖，若有必须显式声明最小权限",
            "禁止硬编码 secret/credential",
            "审计日志与文档示例禁止输出敏感值",
        ]
    },
    5: {
        "## 执行规格": [
            "工具文档回填以 tool_id 为主键：registry/docs/ledger 必须同轮更新",
            "状态文件更新具备明确 owner 与写入顺序",
            "变更后必须可追溯到 run_id",
        ]
    },
    6: {
        "## 接口与数据契约": [
            "每个工具必须具备 usage/modification/development 三段结构化契约",
            "工具变更顺序固定为 docs_pre_update -> script_update -> ledger_append -> full_gate",
            "破坏性变更需要升级与迁移说明",
        ]
    },
    7: {
        "## 文件与资产映射": [
            "故障归类优先按 tool_id 定位到 usage/modification/development 文档段",
            "每类故障有固定 triage 入口与锚点路径",
            "缺失审计事件视为阻塞故障",
        ]
    },
    8: {
        "## 实施切片与写入计划": [
            "工具文档回填按 contract/flow/mapping/evidence 四类切片追踪",
            "写入顺序与步骤事件保持一致",
            "审计产物与运行产物路径固定",
        ]
    },
    9: {
        "## 测试与 Hazard 覆盖": [
            "functional/boundary/hazard/regression 四类覆盖",
            "gate 失败即阻塞发布",
            "回归后必须重跑全链路 gate",
        ]
    },
    10: {
        "## 部署与回滚门禁": [
            "发布前必须通过 docs-first 全链路 gate",
            "回滚必须补写 ledger 与审计事件",
            "禁止跳过 gate 直接发布",
        ]
    },
    11: {
        "## 运行与审计 Runbook": [
            "治理 run 必须 start/step/finish 全量事件",
            "结果报告必须带 governance_audit_run_id",
            "目标技能治理前必须先产出审计报告并在用户确认后才进入计划与施工",
            "runbook 主语是工具文档维护而非治理叙事：先定位 tool_id，再执行文档与脚本同步",
            "治理交付验收必须包含 target outcome lint（字段/路径/脚本/文档非空/traceability）PASS",
            "目标技能 `SKILL.md` 采用 no-trace 策略，不注入 Meta marker/合同块",
            "故障优先读取 runs/<run_id>.json",
        ]
    },
    12: {
        "## 运营策略与例外处理": [
            "例外策略必须可审计",
            "人工例外不能覆盖基础 gate",
            "target outcome lint 属于基础 gate，不允许被跳过",
            "所有例外需要补写原因与恢复动作",
        ]
    },
}

BATCH_ROLLOUT_SIGNAL_FILES = (
    "scripts/batch_governance_migrate.py",
    "scripts/governance_scope_registry.py",
)

ANCHOR_FIELD_KEYS = [
    "tool_anchor_refs",
    "script_anchor_refs",
    "asset_anchor_refs",
    "evidence_anchor_refs",
]

DEFAULT_TOOL_TO_SCRIPT: dict[str, str] = {
    "init_tooling_governance_instance": "scripts/init_tooling_governance_instance.py",
    "tooling_governance_lint": "scripts/tooling_governance_lint.py",
    "tooling_governance_context_backfill": "scripts/tooling_governance_context_backfill.py",
    "tooling_governance_apply_change": "scripts/tooling_governance_apply_change.py",
    "tooling_governance_auto_writeback": "scripts/tooling_governance_auto_writeback.py",
    "tooling_docs_query": "scripts/tooling_docs_query.py",
    "tooling_docs_record": "scripts/tooling_docs_record.py",
    "tooling_change_ledger": "scripts/tooling_change_ledger.py",
    "tooling_change_impact_mapper": "scripts/tooling_change_impact_mapper.py",
    "batch_governance_migrate": "scripts/batch_governance_migrate.py",
    "governance_audit_log": "scripts/governance_audit_log.py",
    "shared_tooling_runtime_contract": "scripts/shared_tooling_runtime_contract.py",
    "governance_scope_registry": "scripts/governance_scope_registry.py",
    "mstg_l0_l13_linear_writeback": "scripts/mstg_l0_l13_linear_writeback.py",
    "mstg_l0_l13_linear_lint": "scripts/mstg_l0_l13_linear_lint.py",
    "mstg_l0_l13_layer_schema_lint": "scripts/mstg_l0_l13_layer_schema_lint.py",
    "mstg_l0_l13_full_gate_lint": "scripts/mstg_l0_l13_full_gate_lint.py",
    "mstg_target_governance_outcome_lint": "scripts/mstg_target_governance_outcome_lint.py",
    "mstg_target_skill_audit": "scripts/mstg_target_skill_audit.py",
    "mstg_governance_plan_manager": "scripts/mstg_governance_plan_manager.py",
}

TOOL_TO_LAYERS: dict[str, list[int]] = {
    "init_tooling_governance_instance": [0, 1, 2, 3, 6, 10, 11, 12, 13],
    "tooling_governance_lint": [9, 12, 13],
    "tooling_governance_context_backfill": [1, 2, 3, 6, 10, 11, 13],
    "tooling_governance_apply_change": [6, 10, 11, 12, 13],
    "tooling_governance_auto_writeback": [6, 10, 11, 12, 13],
    "tooling_docs_query": [0, 1, 2, 5, 10],
    "tooling_docs_record": [2, 5, 10, 11],
    "tooling_change_ledger": [5, 10, 11, 13],
    "tooling_change_impact_mapper": [6, 10, 11, 12],
    "batch_governance_migrate": [0, 1, 2, 8, 10, 11, 12, 13],
    "governance_audit_log": [8, 10, 11, 12, 13],
    "shared_tooling_runtime_contract": [3, 4, 11],
    "governance_scope_registry": [1, 3, 11, 12, 13],
    "mstg_l0_l13_linear_writeback": [2, 6, 10, 12, 13],
    "mstg_l0_l13_linear_lint": [9, 12, 13],
    "mstg_l0_l13_layer_schema_lint": [9, 12, 13],
    "mstg_l0_l13_full_gate_lint": [9, 12, 13],
    "mstg_target_governance_outcome_lint": [11, 12, 13],
    "mstg_target_skill_audit": [1, 6, 8, 11, 12, 13],
    "mstg_governance_plan_manager": [1, 2, 6, 10, 11, 13],
}

ASSET_TO_LAYERS: dict[str, list[int]] = {
    "runtime/TOOL_REGISTRY.yaml": [1, 2, 6, 12, 13],
    "runtime/TOOL_DOCS_STRUCTURED.yaml": [0, 1, 2, 5, 10, 12, 13],
    "runtime/TOOL_CHANGE_LEDGER.jsonl": [5, 10, 11, 13],
    "runtime/TOOLING_GOVERNANCE_STATE.yaml": [5, 6, 10, 11, 13],
    "runtime/TOOLBOX_INJECTION_MANIFEST.yaml": [1, 2, 6, 11, 13],
    "runtime/L0_L13_LINEAR_INDEX.yaml": [0, 1, 2, 13],
    "assets/schemas/tool_registry.schema.json": [2, 6, 12],
    "assets/schemas/tool_docs_structured.schema.json": [2, 6, 12],
    "assets/schemas/change_event.schema.json": [2, 10, 12],
    "assets/chains/milestone_chain_packets.yaml": [1, 2, 13],
    "docs/L1/chains": [1, 2, 13],
    "docs/L2/chains": [2, 13],
    "docs/chains/MILESTONE_CHAIN_MAP.md": [0, 1, 2, 13],
    "docs/tooling/TOOL_DOC_SYNC_CONTRACT.md": [1, 2, 10, 12, 13],
    "docs/evolution/SELF_EVOLUTION_TRACEABILITY.md": [1, 6, 10, 11, 13],
    "references/mstg_target_outcome_lint_contract.yaml": [11, 12, 13],
}

EVIDENCE_TO_LAYERS: dict[str, list[int]] = {
    "docs/L13/README.md": list(range(14)),
    "docs/L1/chains": [1, 2, 13],
    "docs/L2/chains": [2, 13],
    "runtime/TOOL_CHANGE_LEDGER.jsonl": [5, 6, 8, 10, 11, 12, 13],
    "runtime/TOOL_DOCS_STRUCTURED.yaml": [0, 1, 2, 5, 10, 12, 13],
    "runtime/L0_L13_LINEAR_INDEX.yaml": [0, 1, 2, 13],
    "docs/chains/MILESTONE_CHAIN_MAP.md": [1, 2, 13],
    "docs/tooling/TOOL_DOC_SYNC_CONTRACT.md": [1, 2, 10, 12, 13],
    "docs/evolution/SELF_EVOLUTION_TRACEABILITY.md": [1, 6, 10, 11, 13],
}

SCRIPT_EXTRA_TO_LAYERS: dict[str, list[int]] = {
    "scripts/mstg_three_mode_workflow.py": [1, 2, 6, 10, 11, 12, 13],
    "scripts/mstg_target_skill_audit_helpers.py": [1, 6, 8, 11, 12, 13],
}

ANCHOR_ASSET_FALLBACKS = [
    "runtime/L0_L13_LINEAR_INDEX.yaml",
    "runtime/TOOL_DOCS_STRUCTURED.yaml",
    "runtime/TOOL_REGISTRY.yaml",
]

ANCHOR_TOOL_FALLBACKS = [
    "tg_tooling_governance_lint",
    "tooling_governance_lint",
    "tg_tooling_docs_query",
    "tooling_docs_query",
]
