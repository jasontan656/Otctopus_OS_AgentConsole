# L0 Tooling Documentation Layer: L0 Scope and Identity

## Layer Intent
Define target-skill tool-doc backfill scope, ownership, and inventory baseline.

## Managed Skill Context
- managed_skill: `2-Task-runtime-selfcheck`
- layer_id: `L0`
- layer_anchor: `l0::composite_layer`

## Detailed Narrative
L0 must convert upstream constraints into downstream executable tool documentation statements.
This layer must map to target-skill tools and remain deterministic via structured runtime artifacts.

## AI 阅读目录（目标技能 toolbox 视角）
- 第一步：读 `Toolbox 能力总览`，先理解工具分层与能力边界。
- 第二步：读 `快速使用入口`，直接复制命令验证工具。
- 第三步：读 `开发过程（脚本反向推导写入）`，按固定链路做改动。
- 第四步：读 `运行维护入口`，完成 gate 与闭环验收。

## 文档链路总览
- 骨干链路（backbone）: `1` 条
  - `L0 -> L1 -> ... -> L13`
- 工具文档母链（L1/L2）: `4` 条
  - `chain_tool_inventory_baseline`: 先把目标技能现有工具做完整盘点（tool_id/entrypoint/domain/owner），建立文档回填索引基线。
  - `chain_usage_contract_backfill`: 为每个工具补齐可执行的使用文档（命令示例、输入输出、锚点映射），让接手者可直接运行。
  - `chain_modification_development_backfill`: 为每个工具补齐修改与开发文档（更新流程、必更文档、开发留痕），降低后续改造摩擦。
  - `chain_sync_traceability_closure`: 确保 registry/docs/machine-map/ledger 同步并通过 gate/outcome lint，形成可审计闭环。
- 总链路数（骨干 + 里程碑）: `5`

## Toolbox 能力总览（目标技能）
- 主语约束：本层描述“本技能 toolbox 能做什么、如何开发与运维”，不是治理流程叙事。
- managed_tool_count: `25`
- toolbox_scripts_dir: `tooling_governance/default/scripts`
- toolbox_instance_dir: `tooling_governance/default`
- source_of_truth: `runtime/TOOL_REGISTRY.yaml` + `runtime/TOOL_DOCS_STRUCTURED.yaml`
- `governance_toolbox`: `23` tools
- `skill_tool`: `2` tools
- representative_tools:
- `runtime_pain_batch` | domain:`skill_tool` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `scripts/runtime_pain_batch.py`
  - quick_command: `python3 scripts/runtime_pain_batch.py --help`
  - usage_summary: Governed tool contract for runtime_pain_batch; keep script/docs/ledger synchronized during self-evolution.
- `runtime_pain_narrative` | domain:`skill_tool` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `scripts/runtime_pain_narrative.py`
  - quick_command: `python3 scripts/runtime_pain_narrative.py --help`
  - usage_summary: Governed tool contract for runtime_pain_narrative; keep script/docs/ledger synchronized during self-evolution.
- `tg_governance_audit_log` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/governance_audit_log.py`
  - quick_command: `python3 tooling_governance/default/scripts/governance_audit_log.py --help`
  - usage_summary: Governed tool contract for tg_governance_audit_log; keep script/docs/ledger synchronized during self-evolution.
- `tg_mstg_l0_l13_full_gate_lint` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py`
  - quick_command: `python3 tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py --help`
  - usage_summary: Governed tool contract for tg_mstg_l0_l13_full_gate_lint; keep script/docs/ledger synchronized during self-evolution.
- `tg_mstg_l0_l13_layer_schema_lint` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py`
  - quick_command: `python3 tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py --help`
  - usage_summary: Governed tool contract for tg_mstg_l0_l13_layer_schema_lint; keep script/docs/ledger synchronized during self-evolution.
- `tg_mstg_l0_l13_linear_composite` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/mstg_l0_l13_linear_composite.py`
  - quick_command: `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_composite.py --help`
  - usage_summary: Governed tool contract for tg_mstg_l0_l13_linear_composite; keep script/docs/ledger synchronized during self-evolution.
- `tg_mstg_l0_l13_linear_flow` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/mstg_l0_l13_linear_flow.py`
  - quick_command: `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_flow.py --help`
  - usage_summary: Governed tool contract for tg_mstg_l0_l13_linear_flow; keep script/docs/ledger synchronized during self-evolution.
- `tg_mstg_l0_l13_linear_layers` | domain:`governance_toolbox` | owner:`2-Task-runtime-selfcheck`
  - entrypoint: `tooling_governance/default/scripts/mstg_l0_l13_linear_layers.py`
  - quick_command: `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_layers.py --help`
  - usage_summary: Governed tool contract for tg_mstg_l0_l13_linear_layers; keep script/docs/ledger synchronized during self-evolution.

## 快速使用入口（AI 直接执行）
- `runtime_pain_batch` -> `python3 scripts/runtime_pain_batch.py --help`
- `runtime_pain_narrative` -> `python3 scripts/runtime_pain_narrative.py --help`
- `tg_governance_audit_log` -> `python3 tooling_governance/default/scripts/governance_audit_log.py --help`
- `tg_mstg_l0_l13_full_gate_lint` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py --help`
- `tg_mstg_l0_l13_layer_schema_lint` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_layer_schema_lint.py --help`
- `tg_mstg_l0_l13_linear_composite` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_composite.py --help`
- `tg_mstg_l0_l13_linear_flow` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_flow.py --help`
- `tg_mstg_l0_l13_linear_layers` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_layers.py --help`
- `tg_mstg_l0_l13_linear_lint` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_lint.py --help`
- `tg_mstg_l0_l13_linear_profile` -> `python3 tooling_governance/default/scripts/mstg_l0_l13_linear_profile.py --help`

## 开发过程（脚本反向推导写入）
- Step 1: 更新 `runtime/TOOL_REGISTRY.yaml` 与 `runtime/TOOL_DOCS_STRUCTURED.yaml`，固定 tool_id 事实基线。
- Step 2: 执行 docs-first 变更链（文档 -> 脚本 -> ledger -> gate）。
- Step 3: 运行 `tooling_governance_auto_writeback.py` 回填 L0-L13。
- Step 4: 运行 full gate + target outcome lint，确认路径和锚点可解析。
- Step 5: 追加 `runtime/TOOL_CHANGE_LEDGER.jsonl` 并归档审计结果。

## 运行维护入口
- `python3 tooling_governance/default/scripts/mstg_l0_l13_full_gate_lint.py --instance-root tooling_governance/default`
- `python3 tooling_governance/default/scripts/mstg_target_governance_outcome_lint.py --instance-root tooling_governance/default`
- `python3 tooling_governance/default/scripts/tooling_docs_query.py --tool-id <tool_id>`

## 上下游映射（what comes next and why）
- 上游来源: `none`
- 下游去向: `L1`
- 下一步是什么: 把 L0 的输出交给 `L1`，保持目录化链路可审计。

## Machine Map
```yaml
layer_id: L0
anchor: l0::composite_layer
dependency: []
input:
  - governance baseline
output:
  - L0 tool-doc deliverable
  - handoff package for L1
acceptance:
  - Layer objective can be explained by human and agent
  - Machine map fields are complete and extractable
  - Next layer handoff is explicit and deterministic
upstream: none
downstream: L1
decision_control_ref: docs/L4/README.md#决策与控制点
execution_spec_ref: docs/L5/README.md#执行规格
acceptance_evidence_ref: docs/L13/README.md#验收证据与闭环归档
tool_anchor_refs:
  - tg_tooling_docs_query
script_anchor_refs:
  - tooling_governance/default/scripts/tooling_docs_query.py
asset_anchor_refs:
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
evidence_anchor_refs:
  - runtime/TOOL_DOCS_STRUCTURED.yaml
code_mapping_refs:
  - docs/chains/MILESTONE_CHAIN_MAP.md
  - runtime/TOOL_DOCS_STRUCTURED.yaml
  - tooling_governance/default/scripts/tooling_docs_query.py
path: docs/L0/README.md
doc_chain_topology:
  backbone_chain_count: 1
  milestone_chain_count: 4
  milestone_chains:
    - chain_tool_inventory_baseline
    - chain_usage_contract_backfill
    - chain_modification_development_backfill
    - chain_sync_traceability_closure
managed_tool_count: 25
managed_tool_ids:
  - runtime_pain_batch
  - runtime_pain_narrative
  - tg_governance_audit_log
  - tg_mstg_l0_l13_full_gate_lint
  - tg_mstg_l0_l13_layer_schema_lint
  - tg_mstg_l0_l13_linear_composite
  - tg_mstg_l0_l13_linear_flow
  - tg_mstg_l0_l13_linear_layers
  - tg_mstg_l0_l13_linear_lint
  - tg_mstg_l0_l13_linear_profile
  - tg_mstg_l0_l13_linear_writeback
  - tg_mstg_l0_l13_writeback_contracts
  - tg_mstg_target_governance_outcome_lint
  - tg_mstg_target_outcome_lint_helpers
  - tg_mstg_target_skill_audit_helpers
  - tg_mstg_three_mode_workflow
  - tg_mstg_yaml
  - tg_tooling_change_impact_mapper
  - tg_tooling_change_ledger
  - tg_tooling_docs_query
  - tg_tooling_docs_record
  - tg_tooling_governance_apply_change
  - tg_tooling_governance_auto_writeback
  - tg_tooling_governance_context_backfill
  - tg_tooling_governance_lint
quickstart_command_count: 20
tool_docs_source_of_truth:
  - runtime/TOOL_REGISTRY.yaml
  - runtime/TOOL_DOCS_STRUCTURED.yaml
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
