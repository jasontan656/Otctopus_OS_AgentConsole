# L1 Tooling Documentation Layer: L1 Interface Contract

## Layer Intent
Define parent chains for tool-doc maintenance contracts and handoff boundaries.

## Managed Skill Context
- managed_skill: `Word-docs`
- layer_id: `L1`
- layer_anchor: `l1::composite_layer`

## Detailed Narrative
L1 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 工具文档母链定义（L1）
- milestone_chain_count: `4`
- chain_1: `chain_tool_inventory_baseline`
  - 里程碑目标: 先把目标技能现有工具做完整盘点（tool_id/entrypoint/domain/owner），建立文档回填索引基线。
  - 文档焦点: 工具盘点与分类基线（tool_id/entrypoint/domain/owner）
  - 文档承载: `docs/L1/chains/chain_tool_inventory_baseline.md`
- chain_2: `chain_usage_contract_backfill`
  - 里程碑目标: 为每个工具补齐可执行的使用文档（命令示例、输入输出、锚点映射），让接手者可直接运行。
  - 文档焦点: 工具使用文档回填（命令、输入、输出、usage锚点）
  - 文档承载: `docs/L1/chains/chain_usage_contract_backfill.md`
- chain_3: `chain_modification_development_backfill`
  - 里程碑目标: 为每个工具补齐修改与开发文档（更新流程、必更文档、开发留痕），降低后续改造摩擦。
  - 文档焦点: 工具修改与开发文档回填（workflow、required_docs、development记录）
  - 文档承载: `docs/L1/chains/chain_modification_development_backfill.md`
- chain_4: `chain_sync_traceability_closure`
  - 里程碑目标: 确保 registry/docs/machine-map/ledger 同步并通过 gate/outcome lint，形成可审计闭环。
  - 文档焦点: 工具文档同步闭环（registry/docs/anchors/ledger/gate）
  - 文档承载: `docs/L1/chains/chain_sync_traceability_closure.md`

## Toolbox 接口面编排
- AI 使用者入口：从 usage 段拿命令、输入、输出。
- AI 开发者入口：从 modification/development 段拿更新顺序和 required_docs。
- 运维入口：通过 `tooling_governance_apply_change.py` 执行统一变更链。

## 工具文档维护入口（固定母线）
- 每条母链都必须落到目标技能工具文档维护动作，不能只描述治理流程动作。
- 目标技能脚本变更默认走 `tooling_governance_auto_writeback.py`（内部调用 `tooling_governance_apply_change.py`）。
- 固定顺序：先文档更新，再脚本更新，再运维/ledger，最后 gate。
- 工具自进化必须留痕：同步 `runtime/TOOL_DOCS_STRUCTURED.yaml`、`runtime/TOOL_REGISTRY.yaml`、machine-map anchors，并追加 `runtime/TOOL_CHANGE_LEDGER.jsonl`。
- 本层关键脚本目录：`tooling_governance/default/scripts`。

## 上下游映射（what comes next and why）
- 上游来源: `L0`
- 下游去向: `L2`
- 下一步是什么: 把 L1 的输出交给 `L2`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L1
anchor: l1::composite_layer
dependency:
  - L0
input:
  - L0 outputs
output:
  - L1 tool-doc deliverable
  - handoff package for L2
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L0
downstream: L2
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_tooling_docs_query
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
asset_anchor_refs:
  - assets/chains/milestone_chain_packets.yaml
  - docs/L1/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
evidence_anchor_refs:
  - docs/L1/chains
  - docs/L1/chains/chain_modification_development_backfill.md
  - docs/L1/chains/chain_sync_traceability_closure.md
  - docs/L1/chains/chain_tool_inventory_baseline.md
  - docs/L1/chains/chain_usage_contract_backfill.md
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - assets/chains/milestone_chain_packets.yaml
  - docs/L1/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L1/README.md
milestone_chain_count: 4
milestone_chains:
  - chain_tool_inventory_baseline
  - chain_usage_contract_backfill
  - chain_modification_development_backfill
  - chain_sync_traceability_closure
l1_chain_docs:
  chain_tool_inventory_baseline: docs/L1/chains/chain_tool_inventory_baseline.md
  chain_usage_contract_backfill: docs/L1/chains/chain_usage_contract_backfill.md
  chain_modification_development_backfill: docs/L1/chains/chain_modification_development_backfill.md
  chain_sync_traceability_closure: docs/L1/chains/chain_sync_traceability_closure.md
governance_entrypoint_contracts:
  - toolbox_injection
  - apply_change_sequence
tool_doc_chain_focus:
  chain_tool_inventory_baseline: 工具盘点与分类基线（tool_id/entrypoint/domain/owner）
  chain_usage_contract_backfill: 工具使用文档回填（命令、输入、输出、usage锚点）
  chain_modification_development_backfill: 工具修改与开发文档回填（workflow、required_docs、development记录）
  chain_sync_traceability_closure: 工具文档同步闭环（registry/docs/anchors/ledger/gate）
tool_domain_counts:
  governance_toolbox: 23
  skill_tool: 1
toolbox_scripts_dir: tooling_governance/default/scripts
workflow_steps_ranked:
  - docs_pre_update
  - script_update
  - tool_docs_registry_sync_check
  - machine_map_anchor_sync
  - ledger_append
  - full_gate_lint
```
