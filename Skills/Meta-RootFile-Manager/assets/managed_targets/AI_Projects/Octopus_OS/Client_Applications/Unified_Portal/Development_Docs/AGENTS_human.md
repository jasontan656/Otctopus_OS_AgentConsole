---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_octopus_os_client_applications_unified_portal_development_docs_agents
doc_type: topic_atom
topic: Agents
anchors:
- target: ../../../../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications/Unified_Portal/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前模块开发文档与施工闭环之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/AGENTS.md" --json`

2. 当前容器定位
- 当前对象是 `Unified_Portal` 的 `Development_Docs` 受管入口。
- 具体 docs/codebase roots、逻辑主题标识与 hook 锚点以 `Part B` machine payload 为准。

3. DevFlow 闭环入口
- 当前模块开发闭环由 `$Workflow-OctopusOS-DevFlow` 驱动。
- 阶段前置检查、读物边界、命令入口与 graph 角色，不在本文件重复展开；一律从该 skill 的 CLI JSON contract 读取。

4. 治理链约束
- 本文件只承载外部 `Part A`。
- 更新本文件必须通过 `$Meta-RootFile-Manager` 的 `collect` / `push` / `scaffold` 闭环。
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications/Unified_Portal/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "devflow_module_docs_entry",
  "default_meta_skill_order": [
    "$Dev-VUE3-WebUI-Frontend (run lint always for mother doc edits.)"
  ],
  "governed_container": {
    "development_docs_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs",
    "codebase_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal",
    "module_dir": "Unified_Portal"
  },
  "workflow_contract": {
    "required_skill": "Workflow-OctopusOS-DevFlow"
  },
  "turn_end_contract_hooks": {
    "frontend_skill_backflow": {
      "enabled": true,
      "target_skill": "Dev-VUE3-WebUI-Frontend",
      "scope_root": "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/Unified_Portal/Development_Docs/mother_doc/04_frontend_contract_layer",
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
