# L3 Tooling Documentation Layer: L3 Dependency Runtime Policy

## Layer Intent
Define runtime/dependency policy for tool-doc maintenance scripts.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L3`
- layer_anchor: `l3::composite_layer`

## Detailed Narrative
L3 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 共享运行时与依赖策略（Toolbox）
- 治理脚本目录: `tooling_governance/default/scripts`
- 业务脚本（skill_tool）与治理脚本（governance_toolbox）必须分层，禁止职责混写。
- 依赖策略：优先复用 shared tooling runtime，避免重复造轮子。
- tool_id 对应脚本入口与文档锚点必须保持一致。

## 依赖边界快照
- `governance_toolbox`: `23` tools
- `skill_tool`: `2` tools

## 上下游映射（what comes next and why）
- 上游来源: `L2`
- 下游去向: `L4`
- 下一步是什么: 把 L3 的输出交给 `L4`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L3
anchor: l3::composite_layer
dependency:
  - L2
input:
  - L2 outputs
output:
  - L3 tool-doc deliverable
  - handoff package for L4
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L2
downstream: L4
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_tooling_governance_context_backfill
script_anchor_refs:
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
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
  - tooling_governance/default/scripts/tooling_governance_context_backfill.py
path: docs/L3/README.md
shared_runtime_policy:
  - shared_venv
  - dependency_reuse
  - non_conflicting_toolbox
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
