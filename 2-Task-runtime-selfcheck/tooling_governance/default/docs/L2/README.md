# L2 Tooling Documentation Layer: L2 IO Schema Contract

## Layer Intent
Define per-chain tool-doc packets and required usage/modification/development schema.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L2`
- layer_anchor: `l2::composite_layer`

## Detailed Narrative
L2 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 工具文档子链包映射（L2）
- 对 `chain_tool_inventory_baseline` 的细化里程碑:
  - `m1_collect_tool_registry_snapshot`
  - `m2_scan_target_entrypoints`
  - `m3_tool_domain_owner_classification`
  - `m4_anchor_binding_baseline`
  - `m5_inventory_acceptance`
  - 链路包文档: `docs/L2/chains/chain_tool_inventory_baseline/README.md`
- 对 `chain_usage_contract_backfill` 的细化里程碑:
  - `m1_usage_command_examples`
  - `m2_usage_inputs_outputs`
  - `m3_usage_doc_anchor_binding`
  - `m4_usage_nonempty_validation`
  - `m5_usage_contract_gate`
  - 链路包文档: `docs/L2/chains/chain_usage_contract_backfill/README.md`
- 对 `chain_modification_development_backfill` 的细化里程碑:
  - `m1_modification_workflow_contract`
  - `m2_required_docs_matrix`
  - `m3_sync_contract_and_guardrails`
  - `m4_development_record_policy`
  - `m5_modification_development_gate`
  - 链路包文档: `docs/L2/chains/chain_modification_development_backfill/README.md`
- 对 `chain_sync_traceability_closure` 的细化里程碑:
  - `m1_registry_docs_sync_check`
  - `m2_machine_map_anchor_sync`
  - `m3_change_ledger_traceability`
  - `m4_gate_and_outcome_lint`
  - `m5_l13_closure_archive`
  - 链路包文档: `docs/L2/chains/chain_sync_traceability_closure/README.md`

## Toolbox 字段合同覆盖率
- usage_coverage: `25/25`
- modification_coverage: `25/25`
- development_coverage: `25/25`
- 若任一覆盖率低于 tool_count，视为合同未闭环。

## 结构化文档查询与写回接口
- 结构化文档来源: `runtime/TOOL_DOCS_STRUCTURED.yaml`
- 读取接口: `tooling_docs_query.py`
- 写回接口: `tooling_docs_record.py / tooling_change_ledger.py`
- 每个 tool_id 必须具备 `usage/modification/development` 三段。

## 开发流水线（来自工具合同）
- `docs_pre_update`
- `script_update`
- `tool_docs_registry_sync_check`
- `machine_map_anchor_sync`
- `ledger_append`
- `full_gate_lint`

## 锚点映射合同（目标技能）
- 被治理目标技能的 `L0-L13` 文档必须包含并维护：`tool_anchor_refs`、`script_anchor_refs`、`asset_anchor_refs`、`evidence_anchor_refs`。
- 目标技能后续修改时，影响分析必须优先消费 machine map 锚点字段，仅在缺失时才允许回退到规则推断。
- 每次工具演进必须同步工具文档锚点（`usage/modification/development`）与 machine-map 锚点，禁止脚本文档漂移。

## 上下游映射（what comes next and why）
- 上游来源: `L1`
- 下游去向: `L3`
- 下一步是什么: 把 L2 的输出交给 `L3`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L2
anchor: l2::composite_layer
dependency:
  - L1
input:
  - L1 outputs
output:
  - L2 tool-doc deliverable
  - handoff package for L3
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L1
downstream: L3
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_mstg_l0_l13_linear_writeback
  - tg_tooling_docs_query
  - tg_tooling_docs_record
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
asset_anchor_refs:
  - assets/chains/milestone_chain_packets.yaml
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/L1/chains
  - docs/L2/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
evidence_anchor_refs:
  - docs/L1/chains
  - docs/L2/chains
  - docs/L2/chains/chain_modification_development_backfill/README.md
  - docs/L2/chains/chain_sync_traceability_closure/README.md
  - docs/L2/chains/chain_tool_inventory_baseline/README.md
  - docs/L2/chains/chain_usage_contract_backfill/README.md
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - assets/chains/milestone_chain_packets.yaml
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/L1/chains
  - docs/L2/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L2/README.md
l2_sub_milestone_packets:
  chain_tool_inventory_baseline:
    - m1_collect_tool_registry_snapshot
    - m2_scan_target_entrypoints
    - m3_tool_domain_owner_classification
    - m4_anchor_binding_baseline
    - m5_inventory_acceptance
  chain_usage_contract_backfill:
    - m1_usage_command_examples
    - m2_usage_inputs_outputs
    - m3_usage_doc_anchor_binding
    - m4_usage_nonempty_validation
    - m5_usage_contract_gate
  chain_modification_development_backfill:
    - m1_modification_workflow_contract
    - m2_required_docs_matrix
    - m3_sync_contract_and_guardrails
    - m4_development_record_policy
    - m5_modification_development_gate
  chain_sync_traceability_closure:
    - m1_registry_docs_sync_check
    - m2_machine_map_anchor_sync
    - m3_change_ledger_traceability
    - m4_gate_and_outcome_lint
    - m5_l13_closure_archive
l2_chain_docs:
  chain_tool_inventory_baseline: docs/L2/chains/chain_tool_inventory_baseline/README.md
  chain_usage_contract_backfill: docs/L2/chains/chain_usage_contract_backfill/README.md
  chain_modification_development_backfill: docs/L2/chains/chain_modification_development_backfill/README.md
  chain_sync_traceability_closure: docs/L2/chains/chain_sync_traceability_closure/README.md
structured_doc_contracts:
  - tool_registry_sync
  - tool_docs_structured_sync
  - ledger_sync
target_docs_anchor_required: true
required_anchor_fields:
  - tool_anchor_refs
  - script_anchor_refs
  - asset_anchor_refs
  - evidence_anchor_refs
tool_doc_required_sections:
  - usage
  - modification
  - development
tool_doc_section_coverage:
  usage: 25
  modification: 25
  development: 25
tool_domain_counts:
  governance_toolbox: 23
  skill_tool: 2
toolbox_scripts_dir: tooling_governance/default/scripts
workflow_steps_ranked:
  - docs_pre_update
  - script_update
  - tool_docs_registry_sync_check
  - machine_map_anchor_sync
  - ledger_append
  - full_gate_lint
```
