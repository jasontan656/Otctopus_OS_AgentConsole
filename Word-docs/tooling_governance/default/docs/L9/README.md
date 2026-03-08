# L9 Tooling Documentation Layer: L9 Test and Regression Matrix

## Layer Intent
Define regression matrix for tool-doc synchronization and gates.

## Managed Skill Context
- managed_skill: `Word-docs`
- layer_id: `L9`
- layer_anchor: `l9::composite_layer`

## Detailed Narrative
L9 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 测试与 Hazard 覆盖
- 至少覆盖 functional/boundary/hazard/regression 四类风险。
- gate 失败视为阻塞，不允许继续 release。

## 测试与回归矩阵
- functional: 业务工具命令可执行且输出结构化结果。
- schema: L0-L13 machine-map 字段完整、锚点可解析。
- regression: docs/registry/ledger 同步保持成立。
- release_gate: full_gate + target_outcome_lint 同时 PASS。

## 推荐最小回归命令
- `python3 tooling_governance/default/scripts/tooling_governance_lint.py --instance-root tooling_governance/default`
- `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py --instance-root tooling_governance/default`
- `python3 tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py --instance-root tooling_governance/default`
- `python3 tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py --instance-root tooling_governance/default`

## 上下游映射（what comes next and why）
- 上游来源: `L8`
- 下游去向: `L10`
- 下一步是什么: 把 L9 的输出交给 `L10`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L9
anchor: l9::composite_layer
dependency:
  - L8
input:
  - L8 outputs
output:
  - L9 tool-doc deliverable
  - handoff package for L10
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L8
downstream: L10
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_mstg_l0_l13_full_gate_lint
  - tg_mstg_l0_l13_layer_schema_lint
  - tg_mstg_l0_l13_linear_lint
  - tg_tooling_governance_lint
script_anchor_refs:
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
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
  - tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py
  - tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py
  - tooling_governance/default/scripts/tooling_governance_lint.py
path: docs/L9/README.md
test_hazard_matrix:
  - functional
  - boundary
  - hazard
  - regression
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
