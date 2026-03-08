# L8 Tooling Documentation Layer: L8 Observability and Log Policy

## Layer Intent
Define observable events and evidence for tool-doc maintenance runs.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L8`
- layer_anchor: `l8::composite_layer`

## Detailed Narrative
L8 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 实施切片与写入计划
- 先切分 contract/flow/mapping/evidence 四类写入切片，再逐项执行。
- 每个切片完成后立即记录可观测证据，禁止批量盲写。

## 可观测性与日志合同
- 运行事件必须可追溯到 run_id、plan_id、tool_id、变更摘要。
- 审计轨迹由 `GOVERNANCE_AUDIT_LOG.jsonl` + `runs/<run_id>.json` 组成。
- 文档闭环证据需回指 L1/L2/L13 与 runtime 索引资产。

## 观测指标（最低集）
- managed_tool_count: `25`
- command_sample_count: `10`
- workflow_step_count: `6`

## 上下游映射（what comes next and why）
- 上游来源: `L7`
- 下游去向: `L9`
- 下一步是什么: 把 L8 的输出交给 `L9`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L8
anchor: l8::composite_layer
dependency:
  - L7
input:
  - L7 outputs
output:
  - L8 tool-doc deliverable
  - handoff package for L9
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L7
downstream: L9
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_governance_audit_log
script_anchor_refs:
  - scripts/mstg_target_skill_audit_helpers.py
  - tooling_governance/default/scripts/governance_audit_log.py
asset_anchor_refs:
  - assets/chains/milestone_chain_packets.yaml
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/L1/chains
  - docs/L2/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
evidence_anchor_refs:
  - runtime/TOOL_CHANGE_LEDGER.jsonl
code_mapping_refs:
  - assets/chains/milestone_chain_packets.yaml
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/L1/chains
  - docs/L2/chains
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
  - scripts/mstg_target_skill_audit_helpers.py
  - tooling_governance/default/scripts/governance_audit_log.py
path: docs/L8/README.md
write_slices:
  - contract_slice
  - flow_slice
  - mapping_slice
  - evidence_slice
  - audit_trace_slice
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
