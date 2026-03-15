---
doc_id: workflow_centralflow2_octppusos.assets_templates_agents_external_agents_compact_backup
doc_type: example_doc
topic: External Agents Compact Backup
anchors:
- target: ./EXTERNAL_AGENTS.md
  relation: backup_of
  direction: lateral
  reason: Compact backup copy kept inside the skill for future direct injection.
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前模块开发文档、任务包、证据回写与 acceptance 收口之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "{{external_agents_path}}" --json`

2. 当前受管边界
- 当前 repo root 边界：`{{target_root}}`
- 当前开发文档根：`{{development_docs_root}}`
- 当前代码对象根：`{{codebase_root}}`
- 当前受管 docs root：`{{module_docs_root}}`
- 当前逻辑主题标识：`{{module_dir}}`
- mother doc root：`{{mother_doc_root}}`
- execution packs root：`{{construction_plan_root}}`
- graph root：`{{graph_runtime_root}}`

3. DevFlow 闭环入口
- 当前模块的开发文档、任务包、graph、evidence 与 acceptance 闭环由 `$Workflow-CentralFlow2-OctppusOS` 治理。
- 进入任何阶段前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py target-runtime-contract --target-root "{{target_root}}" --development-docs-root "{{development_docs_root}}" --docs-root "{{module_docs_root}}" --module-dir "{{module_dir}}" --json`
- 然后必须运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|construction_plan|implementation|acceptance> --target-root "{{target_root}}" --development-docs-root "{{development_docs_root}}" --docs-root "{{module_docs_root}}" --module-dir "{{module_dir}}" --json`
- 若当前模块已经存在 mother_doc、编号归档、execution packs 或 graph，必须先复用当前脉络；禁止另起脱节文档线。
- 若模块容器已具备使用条件但缺少 `AGENTS.md`、mother_doc、task packs 或 graph，必须先执行 `target-scaffold` 一次性补齐骨架。

4. 阶段读取与切换
- 单阶段执行时，只允许读取顶层常驻文档、当前阶段 checklist，以及当前阶段 `stage-doc-contract / stage-command-contract / stage-graph-contract` 指定的对象。
- 多阶段连续执行时，阶段切换后只保留顶层常驻文档，并且必须重新读取目标阶段 checklist，丢弃上一阶段临时 focus、临时 notes 与阶段局部判断。
- implementation 只允许读取 active pack 与该 pack 显式声明的 `source_mother_doc_refs`；不得通读整个 mother doc 树。
- acceptance 只允许保留交付裁决需要的证据；不得把 implementation 局部调试 focus 直接带入 acceptance。

5. 证据回写与 turn end 闭合
- 证据骨架与任务包文件由 `$Workflow-CentralFlow2-OctppusOS target-scaffold / construction-plan-init` 创建；不得自行发明平替结构。
- implementation 一旦发生真实改动，必须按 active pack 回写 `phase_status.jsonl`、`evidence_registry.json`、`03_validation_and_writeback.md`；必要时回写 `pack_manifest.yaml` 与 `inner_phase_plan.json`。
- 若实现偏离 active pack，必须先回写当前 pack；若设计意图也变化，再回写对应 `doc_role=design_plan` 文档与受影响的 mother doc 原子文档。
- acceptance 必须把 requirement 级裁决回写到当前 acceptance 容器；`implemented=true`、`tested=true`、`witnessed=true` 只能引用当前磁盘上真实存在的证据。
- turn end 不得停在“代码已改但证据未补”的状态；若当前 turn 发生实现、验证、acceptance 或 mother doc 合同变更，必须先补齐本阶段规定的 writeback，再允许结束。
- 若 acceptance 文档领先于真实证据、evidence path 不存在、或 `ref` 状态早于 acceptance closeout / graph postflight，必须先回退或修正，不得伪装成完成态。

6. 治理链约束
- 本文件属于 `Meta-RootFile-Manager` 的受管外部 `AGENTS.md`，外部文件只允许承载 `Part A`。
- 更新本文件时，必须使用 `$Meta-RootFile-Manager` 的 `collect` / `push` / `scaffold` 流程，避免治理链断裂。
- 本文件只负责固定当前模块的 DevFlow 闭环入口、受管边界与 turn end 闭合动作；字段 schema、模板细节、lint 口径与阶段语义一律以下沉 skill 合同为准。
</part_A>
