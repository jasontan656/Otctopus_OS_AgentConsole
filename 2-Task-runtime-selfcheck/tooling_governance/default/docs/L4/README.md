# L4 Tooling Documentation Layer: L4 Secrets and Environment Contract

## Layer Intent
Define env/secret contract for tool-doc workflows and scripts.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L4`
- layer_anchor: `l4::composite_layer`

## Detailed Narrative
L4 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## 决策与控制点
- 任何需要环境变量/密钥的变更必须先声明决策依据与最小权限。
- 涉及敏感信息的写回必须先通过策略审查再进入执行链。

## 环境变量与密钥合同
- 默认策略：toolbox 脚本不依赖 secret；如需要环境变量，必须文档显式声明最小权限。
- 禁止硬编码 key/token/credential 到脚本、文档、ledger 和审计产物。
- strict_sync_contract_tools: `25/25`（三项同步约束全部为 true）。

## 安全写回规则
- 示例命令必须用占位符，不落敏感值。
- gate 发现敏感信息时必须阻塞并先修复。

## 上下游映射（what comes next and why）
- 上游来源: `L3`
- 下游去向: `L5`
- 下一步是什么: 把 L4 的输出交给 `L5`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L4
anchor: l4::composite_layer
dependency:
  - L3
input:
  - L3 outputs
output:
  - L4 tool-doc deliverable
  - handoff package for L5
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: L3
downstream: L5
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_tooling_governance_lint
script_anchor_refs:
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
  - tooling_governance/default/scripts/tooling_governance_lint.py
path: docs/L4/README.md
decision_gates:
  - input_completeness_gate
  - policy_gate
  - evidence_gate
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
