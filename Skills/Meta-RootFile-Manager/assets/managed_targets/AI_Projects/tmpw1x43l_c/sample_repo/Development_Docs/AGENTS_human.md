---
doc_id: workflow_centralflow2_octppusos.assets_templates_agents_external_agents
doc_type: example_doc
topic: External Agents
owner: "由 `$Meta-RootFile-Manager` 作为 `tmpw1x43l_c/sample_repo/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前模块开发文档、任务包、证据回写与 acceptance 收口之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/AGENTS.md" --json`

2. 当前受管边界
- 当前 repo root 边界：`/home/jasontan656/AI_Projects/tmpw1x43l_c`
- 当前开发文档根：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs`
- 当前代码对象根：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo`
- 当前受管 docs root：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs`
- 当前逻辑主题标识：`sample_repo`
- mother doc root：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc`
- execution packs root：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc/execution_atom_plan_validation_packs`
- graph root：`/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/graph`

3. DevFlow 分阶段入口
- 当前模块的开发文档、任务包、graph、evidence 与 acceptance 闭环由 4 个独立技能分别治理：`$Workflow-MotherDoc-OctopusOS`、`$Workflow-ConstructionPlan-OctopusOS`、`$Workflow-Implementation-OctopusOS`、`$Workflow-Acceptance-OctopusOS`。
- 进入任何阶段前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --target-root "/home/jasontan656/AI_Projects/tmpw1x43l_c" --development-docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --module-dir "sample_repo" --json`
- 然后必须运行：
- `mother_doc`: `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-MotherDoc-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage mother_doc --target-root "/home/jasontan656/AI_Projects/tmpw1x43l_c" --development-docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --module-dir "sample_repo" --json`
- `construction_plan`: `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage construction_plan --target-root "/home/jasontan656/AI_Projects/tmpw1x43l_c" --development-docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --module-dir "sample_repo" --json`
- `implementation`: `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage implementation --target-root "/home/jasontan656/AI_Projects/tmpw1x43l_c" --development-docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --module-dir "sample_repo" --json`
- `acceptance`: `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage acceptance --target-root "/home/jasontan656/AI_Projects/tmpw1x43l_c" --development-docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs" --module-dir "sample_repo" --json`
- 若当前模块已经存在 mother_doc、编号归档、execution packs 或 graph，必须先复用当前脉络；禁止另起脱节文档线。
- 若模块容器已具备使用条件但缺少 `AGENTS.md`、mother_doc、task packs 或 graph，必须先执行 `target-scaffold` 一次性补齐骨架。

4. 阶段读取与切换
- 单阶段执行时，只允许读取顶层常驻文档、当前阶段 checklist，以及当前阶段 `stage-doc-contract / stage-command-contract / stage-graph-contract` 指定的对象。
- 多阶段连续执行时，阶段切换后只保留顶层常驻文档，并且必须重新读取目标阶段 checklist，丢弃上一阶段临时 focus、临时 notes 与阶段局部判断。
- implementation 只允许读取 active pack 与该 pack 显式声明的 `source_mother_doc_refs`；不得通读整个 mother doc 树。
- acceptance 只允许保留交付裁决需要的证据；不得把 implementation 局部调试 focus 直接带入 acceptance。

5. 证据回写与 turn end 闭合
- 证据骨架与任务包文件分别由 `$Workflow-MotherDoc-OctopusOS target-scaffold` 与 `$Workflow-ConstructionPlan-OctopusOS construction-plan-init` 创建；不得自行发明平替结构。
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

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `tmpw1x43l_c/sample_repo/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "devflow_module_docs_entry",
  "governed_container": {
    "target_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c",
    "development_docs_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs",
    "codebase_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo",
    "module_dir": "sample_repo",
    "module_docs_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs"
  },
  "workflow_roots": {
    "mother_doc_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc",
    "construction_plan_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc/execution_atom_plan_validation_packs",
    "graph_runtime_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/graph",
    "acceptance_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc/acceptance"
  },
  "workflow_contract": {
    "required_skill": "Workflow-MotherDoc-OctopusOS",
    "required_preflight": [
      "target-runtime-contract",
      "stage-checklist"
    ],
    "reuse_policy": [
      "reuse_existing_mother_doc_when_present",
      "reuse_existing_execution_packs_when_present",
      "reuse_existing_graph_when_present"
    ],
    "governance_chain": [
      "Meta-RootFile-Manager scaffold/collect/push",
      "Workflow-MotherDoc-OctopusOS -> Workflow-ConstructionPlan-OctopusOS -> Workflow-Implementation-OctopusOS -> Workflow-Acceptance-OctopusOS"
    ]
  },
  "turn_end_contract_hooks": {
    "frontend_skill_backflow": {
      "enabled": false,
      "target_skill": "Dev-VUE3-WebUI-Frontend",
      "scope_root": "/home/jasontan656/AI_Projects/tmpw1x43l_c/sample_repo/Development_Docs/mother_doc/04_frontend_contract_layer",
      "required_frontmatter_keys": [
        "skill_sync_target",
        "skill_sync_mode",
        "abstraction_level",
        "backflow_candidate"
      ],
      "qualifying_abstraction_levels": [
        "high",
        "framework"
      ],
      "required_turn_end_actions": [
        "analyze whether edited mother doc atoms changed framework-level frontend contracts",
        "if the edited atoms are marked for Dev-VUE3-WebUI-Frontend backflow, classify them into project-only or skill-worthy abstractions",
        "preserve product mother doc precedence; skill sync is a projection step, not the active requirement source"
      ],
      "product_contract_precedence": true
    }
  }
}
```
</part_B>
