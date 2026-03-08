# L11 Tooling Documentation Layer: L11 Operations Runbook

## Layer Intent
Define operator runbook for daily tool-doc maintenance and incident handling.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L11`
- layer_anchor: `l11::composite_layer`

## Detailed Narrative
L11 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 运行与审计 Runbook（Toolbox 运维）
- 场景 A（新增/替换工具）：先更新 registry + structured docs，再执行 auto_writeback，再跑 gate。
- 场景 B（调整工具用法）：更新 usage 段并同步 machine-map 锚点，再追加 ledger。
- 场景 C（故障修复）：先跑 lint 定位，再按 docs-first 顺序修复，最后重跑 full gate。

## 常用运维命令
- `python3 tooling_governance/default/scripts/tooling_docs_query.py --help`
- `python3 tooling_governance/default/scripts/tooling_docs_record.py --help`
- `python3 tooling_governance/default/scripts/tooling_change_ledger.py --help`
- `python3 tooling_governance/default/scripts/tooling_governance_auto_writeback.py --help`

## 上下游映射（what comes next and why）
- 上游来源: `L10`
- 下游去向: `L12`
- 下一步是什么: 把 L11 的输出交给 `L12`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L11
anchor: l11::composite_layer
dependency:
  - L10
input:
  - L10 outputs
output:
  - L11 tool-doc deliverable
  - handoff package for L12
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L10
downstream: L12
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_governance_audit_log
  - tg_mstg_target_governance_outcome_lint
  - tg_tooling_change_impact_mapper
  - tg_tooling_change_ledger
  - tg_tooling_docs_record
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
asset_anchor_refs:
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
evidence_anchor_refs:
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOL_CHANGE_LEDGER.jsonl
code_mapping_refs:
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_record.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L11/README.md
runbook_controls:
  - observability
  - alerting
  - audit_trace
  - incident_escalation
runbook_entry_scripts:
  - tooling_docs_query.py
  - tooling_docs_record.py
  - tooling_change_ledger.py
  - tooling_governance_auto_writeback.py
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
