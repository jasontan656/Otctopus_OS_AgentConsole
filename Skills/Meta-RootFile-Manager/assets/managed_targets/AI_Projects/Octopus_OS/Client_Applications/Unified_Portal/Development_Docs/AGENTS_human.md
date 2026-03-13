---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_octopus_os_client_applications_unified_portal_development_docs_agents
doc_type: topic_atom
topic: Agents
anchors:
- target: ../../../../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前模块开发文档与施工闭环之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/AGENTS.md" --json`

2. 模块开发文档容器
- 当前 repo/workspace 根边界：`/home/jasontan656/AI_Projects`
- 当前开发文档根：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs`
- 当前代码对象根：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal`
- 当前受管 docs root：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs`
- 当前逻辑主题标识：`Unified_Portal`
- mother doc root：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc`
- execution packs root：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc/execution_atom_plan_validation_packs`
- graph root：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/graph`

3. DevFlow 闭环入口
- 当前模块的开发文档、任务包、evidence 与 acceptance 闭环由 `$Workflow-OctopusOS-DevFlow` 治理。
- 进入任何阶段前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Workflow-OctopusOS-DevFlow/scripts/Cli_Toolbox.py target-runtime-contract --target-root "/home/jasontan656/AI_Projects" --development-docs-root "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs" --docs-root "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs" --module-dir "Unified_Portal" --json`
- 若当前模块已经存在 mother_doc、编号归档、execution packs 或 graph，必须先复用当前脉络；禁止另起脱节文档线。

4. 治理链约束
- 本文件属于 `Meta-RootFile-Manager` 的受管外部 `AGENTS.md`，外部文件只允许承载 `Part A`。
- 更新本文件时，必须使用 `$Meta-RootFile-Manager` 的 `collect` / `push` / `scaffold` 流程，避免治理链断裂。
- 本模块下的开发文档、任务包、graph、evidence 回写和 acceptance 收口，必须同时遵守 `$Workflow-OctopusOS-DevFlow` 的阶段合同。
</part_A>

<part_B>

```json
{
  "entry_role": "devflow_module_docs_entry",
  "governed_container": {
    "target_root": "/home/jasontan656/AI_Projects",
    "development_docs_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs",
    "codebase_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal",
    "module_dir": "Unified_Portal",
    "module_docs_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs"
  },
  "workflow_roots": {
    "mother_doc_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc",
    "construction_plan_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc/execution_atom_plan_validation_packs",
    "graph_runtime_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/graph",
    "acceptance_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc/acceptance"
  },
  "workflow_contract": {
    "required_skill": "Workflow-OctopusOS-DevFlow",
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
      "Workflow-OctopusOS-DevFlow four-stage delivery loop"
    ]
  }
}
```
</part_B>
