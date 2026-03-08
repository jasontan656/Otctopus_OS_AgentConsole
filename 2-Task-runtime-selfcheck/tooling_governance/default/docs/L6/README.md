# L6 Tooling Documentation Layer: L6 Execution and Idempotency Flow

## Layer Intent
Define deterministic docs-first update flow for tool evolution.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L6`
- layer_anchor: `l6::composite_layer`

## Detailed Narrative
L6 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 接口与数据契约
- 输入输出必须对齐 `TOOL_DOCS_STRUCTURED.yaml` 的 usage/modification/development 三段结构。
- 同一 tool_id 的接口字段变更必须同步到 docs 与 ledger。

## 执行与幂等流程（docs-first）
- 单次变更最小闭环：`docs_pre_update -> script_update -> machine_map_anchor_sync -> ledger_append -> full_gate_lint`。
- 幂等要求：重复执行不应破坏已有锚点，不应产生冲突资产。
- 中断恢复：从最近成功步骤继续并重跑 full gate。

## 标准执行顺序（来自工具合同）
- `docs_pre_update`
- `script_update`
- `tool_docs_registry_sync_check`
- `machine_map_anchor_sync`
- `ledger_append`
- `full_gate_lint`

## 命令入口
- `python3 tooling_governance/default/scripts/tooling_governance_apply_change.py --help`
- `python3 tooling_governance/default/scripts/tooling_governance_auto_writeback.py --help`

## 上下游映射（what comes next and why）
- 上游来源: `L5`
- 下游去向: `L7`
- 下一步是什么: 把 L6 的输出交给 `L7`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L6
anchor: l6::composite_layer
dependency:
  - L5
input:
  - L5 outputs
output:
  - L6 tool-doc deliverable
  - handoff package for L7
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L5
downstream: L7
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_mstg_l0_l13_linear_writeback
  - tg_tooling_change_impact_mapper
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
asset_anchor_refs:
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_REGISTRY.yaml
evidence_anchor_refs:
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOL_CHANGE_LEDGER.jsonl
code_mapping_refs:
  - assets/schemas/tool_docs_structured.schema.json
  - assets/schemas/tool_registry.schema.json
  - docs/evolution/SELF_EVOLUTION_TRACEABILITY.md
  - runtime/TOOLBOX_INJECTION_MANIFEST.yaml
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_REGISTRY.yaml
  - scripts/mstg_target_skill_audit_helpers.py
  - scripts/mstg_three_mode_workflow.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_writeback.py
  - tooling_governance/default/scripts/tooling_change_impact_mapper.py
  - tooling_governance/default/scripts/tooling_governance_apply_change.py
  - tooling_governance/default/scripts/tooling_governance_auto_writeback.py
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L6/README.md
interface_contracts:
  - request_response_contract
  - schema_contract
  - versioning_contract
canonical_docs_first_flow:
  - docs_pre_update
  - script_update
  - tool_docs_registry_sync_check
  - machine_map_anchor_sync
  - ledger_append
  - full_gate_lint
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
