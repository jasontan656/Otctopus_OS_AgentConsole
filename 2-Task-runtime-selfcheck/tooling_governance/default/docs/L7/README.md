# L7 Tooling Documentation Layer: L7 Failure and Triage Model

## Layer Intent
Define tool-doc drift/failure taxonomy and triage ownership.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L7`
- layer_anchor: `l7::composite_layer`

## Detailed Narrative
L7 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 文件与资产映射
- 每个故障点必须能映射到 docs/runtime/scripts 的具体路径。
- 先修复映射缺口，再修复业务逻辑，避免二次漂移。

## 失败模型与分诊
- 失败类 1：registry 与 docs 不一致（tool_id 漂移/缺失）。
- 失败类 2：machine-map 锚点字段缺失或路径不可解析。
- 失败类 3：ledger 缺失导致变更不可追溯。
- 失败类 4：target outcome lint 失败。

## 分诊顺序（先证据后修复）
- 先看 `runtime/L0_L13_LINEAR_INDEX.yaml` 识别层级链路问题。
- 再看 `runtime/TOOL_DOCS_STRUCTURED.yaml` 与 `runtime/TOOL_REGISTRY.yaml` 校对 tool_id。
- 最后看 `runtime/TOOL_CHANGE_LEDGER.jsonl` 判断是否丢失变更留痕。

## 上下游映射（what comes next and why）
- 上游来源: `L6`
- 下游去向: `L8`
- 下一步是什么: 把 L7 的输出交给 `L8`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L7
anchor: l7::composite_layer
dependency:
  - L6
input:
  - L6 outputs
output:
  - L7 tool-doc deliverable
  - handoff package for L8
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L6
downstream: L8
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_governance_audit_log
  - tg_mstg_l0_l13_full_gate_lint
  - tg_mstg_l0_l13_layer_schema_lint
  - tg_mstg_l0_l13_linear_lint
  - tg_mstg_l0_l13_linear_writeback
  - tg_mstg_target_governance_outcome_lint
  - tg_tooling_change_impact_mapper
  - tg_tooling_change_ledger
  - tg_tooling_docs_query
  - tg_tooling_docs_record
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_context_backfill
  - tg_tooling_governance_lint
script_anchor_refs:
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
  - tooling_governance/default/scripts/tooling_governance_lint.py
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
  - docs/L13/README.md
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
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
  - tooling_governance/default/scripts/tooling_governance_lint.py
path: docs/L7/README.md
asset_mappings:
  - semantic_to_doc_map
  - semantic_to_script_map
  - anchor_trace_map
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
