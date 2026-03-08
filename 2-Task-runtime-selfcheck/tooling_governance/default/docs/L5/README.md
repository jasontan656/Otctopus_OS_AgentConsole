# L5 Tooling Documentation Layer: L5 State and Storage Contract

## Layer Intent
Define registry/docs/ledger/state synchronization by tool_id.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L5`
- layer_anchor: `l5::composite_layer`

## Detailed Narrative
L5 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 执行规格
- 本层规定状态资产的写入顺序与一致性约束。
- 所有写入动作必须以 tool_id 为主键可回放。

## 状态与存储合同（按资产拆分）
- `runtime/TOOL_REGISTRY.yaml`: 工具清单与 entrypoint 权威源。
- `runtime/TOOL_DOCS_STRUCTURED.yaml`: usage/modification/development 三段合同源。
- `runtime/TOOL_CHANGE_LEDGER.jsonl`: 变更留痕源。
- `runtime/TOOLING_GOVERNANCE_STATE.yaml`: 运行态与治理态记录。

## required_docs 高频集合
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
- 上游来源: `L4`
- 下游去向: `L6`
- 下一步是什么: 把 L5 的输出交给 `L6`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L5
anchor: l5::composite_layer
dependency:
  - L4
input:
  - L4 outputs
output:
  - L5 tool-doc deliverable
  - handoff package for L6
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L4
downstream: L6
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_tooling_change_ledger
  - tg_tooling_docs_query
  - tg_tooling_docs_record
script_anchor_refs:
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
asset_anchor_refs:
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
evidence_anchor_refs:
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - runtime/TOOLING_GOVERNANCE_STATE.yaml
  - runtime/TOOL_CHANGE_LEDGER.jsonl
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - tooling_governance/default/scripts/tooling_change_ledger.py
  - tooling_governance/default/scripts/tooling_docs_query.py
  - tooling_governance/default/scripts/tooling_docs_record.py
path: docs/L5/README.md
execution_contracts:
  - input_contract
  - state_contract
  - output_contract
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
