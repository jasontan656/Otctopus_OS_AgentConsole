# L12 Tooling Documentation Layer: L12 Gates and Lint Controls

## Layer Intent
Define mandatory validation gates for tool-doc consistency.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L12`
- layer_anchor: `l12::composite_layer`

## Detailed Narrative
L12 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 运营策略与例外处理
- 例外只能在证据充分且可审计条件下触发，不得绕过基础门禁。
- 任何例外都必须附带恢复路径与再验证命令。

## Gate 与 lint 控制
- Gate 顺序不可跳过：tooling_governance_lint -> linear_lint -> layer_schema_lint -> full_gate_lint -> target_outcome_lint。
- 任一 gate FAIL，必须先修复再继续；不得带 FAIL 进入 release。
- target outcome lint 是基础门禁，不允许人工豁免覆盖。

## 目标技能结果门禁命令
- `python3 tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py --instance-root tooling_governance/default`

## 上下游映射（what comes next and why）
- 上游来源: `L11`
- 下游去向: `L13`
- 下一步是什么: 把 L12 的输出交给 `L13`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L12
anchor: l12::composite_layer
dependency:
  - L11
input:
  - L11 outputs
output:
  - L12 tool-doc deliverable
  - handoff package for L13
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L11
downstream: L13
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
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_lint
script_anchor_refs:
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_lint.py
asset_anchor_refs:
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
evidence_anchor_refs:
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - assets/schemas/change_event.schema.json
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/tooling/TOOL_DOC_SYNC_CONTRACT.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - runtime/TOOL_REGISTRY.yaml
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/governance_audit_log.py
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_lint.py
path: docs/L12/README.md
operation_exceptions:
  - policy_enforcement
  - manual_override
  - exception_audit
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
