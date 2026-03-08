# Milestone Chain Map

## Purpose
Provide a chain-oriented surface for target-skill tool documentation backfill and maintenance.

## Tool Coverage Baseline
- managed_tool_count: `24`
- source: `runtime/TOOL_REGISTRY.yaml`
- managed_tool_ids:
  - `render_docx`
  - `tg_governance_audit_log`
  - `tg_mstg_l0_l13_full_gate_lint`
  - `tg_mstg_l0_l13_layer_schema_lint`
  - `tg_mstg_l0_l13_linear_composite`
  - `tg_mstg_l0_l13_linear_flow`
  - `tg_mstg_l0_l13_linear_layers`
  - `tg_mstg_l0_l13_linear_lint`
  - `tg_mstg_l0_l13_linear_profile`
  - `tg_mstg_l0_l13_linear_writeback`
  - `tg_mstg_l0_l13_writeback_contracts`
  - `tg_mstg_target_governance_outcome_lint`
  - `tg_mstg_target_outcome_lint_helpers`
  - `tg_mstg_target_skill_audit_helpers`
  - `tg_mstg_three_mode_workflow`
  - `tg_mstg_yaml`
  - `tg_tooling_change_impact_mapper`
  - `tg_tooling_change_ledger`
  - `tg_tooling_docs_query`
  - `tg_tooling_docs_record`
  - `tg_tooling_governance_apply_change`
  - `tg_tooling_governance_auto_writeback`
  - `tg_tooling_governance_context_backfill`
  - `tg_tooling_governance_lint`

## Chains
- chain_id: `chain_tool_inventory_baseline`
- chain_slug: `chain_tool_inventory_baseline`
- tool_doc_focus: 工具盘点与分类基线（tool_id/entrypoint/domain/owner）
- l1_doc: `docs/L1/chains/chain_tool_inventory_baseline.md`
- l2_doc: `docs/L2/chains/chain_tool_inventory_baseline/README.md`
- objective: 先把目标技能现有工具做完整盘点（tool_id/entrypoint/domain/owner），建立文档回填索引基线。
- packets:
  - `m1_collect_tool_registry_snapshot`
  - `m2_scan_target_entrypoints`
  - `m3_tool_domain_owner_classification`
  - `m4_anchor_binding_baseline`
  - `m5_inventory_acceptance`

- chain_id: `chain_usage_contract_backfill`
- chain_slug: `chain_usage_contract_backfill`
- tool_doc_focus: 工具使用文档回填（命令、输入、输出、usage锚点）
- l1_doc: `docs/L1/chains/chain_usage_contract_backfill.md`
- l2_doc: `docs/L2/chains/chain_usage_contract_backfill/README.md`
- objective: 为每个工具补齐可执行的使用文档（命令示例、输入输出、锚点映射），让接手者可直接运行。
- packets:
  - `m1_usage_command_examples`
  - `m2_usage_inputs_outputs`
  - `m3_usage_doc_anchor_binding`
  - `m4_usage_nonempty_validation`
  - `m5_usage_contract_gate`

- chain_id: `chain_modification_development_backfill`
- chain_slug: `chain_modification_development_backfill`
- tool_doc_focus: 工具修改与开发文档回填（workflow、required_docs、development记录）
- l1_doc: `docs/L1/chains/chain_modification_development_backfill.md`
- l2_doc: `docs/L2/chains/chain_modification_development_backfill/README.md`
- objective: 为每个工具补齐修改与开发文档（更新流程、必更文档、开发留痕），降低后续改造摩擦。
- packets:
  - `m1_modification_workflow_contract`
  - `m2_required_docs_matrix`
  - `m3_sync_contract_and_guardrails`
  - `m4_development_record_policy`
  - `m5_modification_development_gate`

- chain_id: `chain_sync_traceability_closure`
- chain_slug: `chain_sync_traceability_closure`
- tool_doc_focus: 工具文档同步闭环（registry/docs/anchors/ledger/gate）
- l1_doc: `docs/L1/chains/chain_sync_traceability_closure.md`
- l2_doc: `docs/L2/chains/chain_sync_traceability_closure/README.md`
- objective: 确保 registry/docs/machine-map/ledger 同步并通过 gate/outcome lint，形成可审计闭环。
- packets:
  - `m1_registry_docs_sync_check`
  - `m2_machine_map_anchor_sync`
  - `m3_change_ledger_traceability`
  - `m4_gate_and_outcome_lint`
  - `m5_l13_closure_archive`
