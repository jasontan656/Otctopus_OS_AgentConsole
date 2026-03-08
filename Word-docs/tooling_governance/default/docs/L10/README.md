# L10 Tooling Documentation Layer: L10 Change Ledger Mapping

## Layer Intent
Define ledger obligations for every tool script/doc update.

## Managed Skill Context
- managed_skill: `Word-docs`
- layer_id: `L10`
- layer_anchor: `l10::composite_layer`

## Detailed Narrative
L10 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 部署与回滚门禁
- 发布前必须通过 full gate 与 target outcome lint。
- 回滚后必须补写 ledger 并重跑 gate，确保状态回正。

## 变更台账映射（L10）
- 每次脚本或文档修改必须追加 ledger 记录。
- ledger 最小字段：`event_id/timestamp_utc/tool_id/change_type/summary`。
- 记录必须可回溯到 docs 与 gate 结果。

## 高频 required_docs（影响面判定）
- `docs/L1/README.md`
- `docs/L1/chains`
- `docs/L2/README.md`
- `docs/L2/chains`
- `docs/L10/README.md`
- `docs/L12/README.md`
- `docs/L13/README.md`
- `docs/tooling/TOOL_DOC_SYNC_CONTRACT.md`
- `docs/evolution/SELF_EVOLUTION_TRACEABILITY.md`

## 上下游映射（what comes next and why）
- 上游来源: `L9`
- 下游去向: `L11`
- 下一步是什么: 把 L10 的输出交给 `L11`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L10
anchor: l10::composite_layer
dependency:
  - L9
input:
  - L9 outputs
output:
  - L10 tool-doc deliverable
  - handoff package for L11
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L9
downstream: L11
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_governance_audit_log
  - tg_mstg_l0_l13_linear_writeback
  - tg_tooling_change_impact_mapper
  - tg_tooling_change_ledger
  - tg_tooling_docs_query
  - tg_tooling_docs_record
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
asset_anchor_refs:
  - assets/schemas/change_event.schema.json
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
evidence_anchor_refs:
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - assets/schemas/change_event.schema.json
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L10/README.md
release_rollback_gates:
  - pre_release_gate
  - rollout_gate
  - rollback_gate
required_docs_ranked:
  - docs/L1/README.md
  - docs/L1/chains
  - docs/L2/README.md
  - docs/L2/chains
  - docs/L10/README.md
  - docs/L12/README.md
  - docs/L13/README.md
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
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
