---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications` 的 client-side 容器合同。
- 本层只承接面向最终用户的界面、交互、页面结构、前端集成与浏览器侧体验规则。

2. 一级读取入口
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --json`

3. 二级分域读取
- hook_identity:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- 若任务实际修改的是 `mother_doc` 真源、文档结构或 client mirror 来源，下一站改读 `/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md`。
- 若进入更深一层具体应用容器且该容器已有自己的 `AGENTS.md`，继续按更深层合同路由。
</contract>

<reminder>
1. 环境提醒
- workspace root 与 `Octopus_OS` repo root 已提供通用环境与上级路由说明，这里不重复展开。

2. 协作提醒
- 本层不承接 `mother_doc` 真源与 client mirror 源面的治理语义。
- 前端实现若需要更细的组件或交互规范，再读取对应前端技能合同。
</reminder>
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "octopus_os_client_applications_contract",
    "contract_scope": "container",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "read_target_contract:/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "govern_surface:client_side_only",
      "exclude_truth_source:mother_doc",
      "route_truth_or_mirror_work_to:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_client_surface_without_file_mutation",
      "default_actions": [
        "read_frontend_contract_when_ui_task"
      ]
    },
    "WRITE_EXEC": {
      "goal": "default to full-coverage edits for the intended change",
      "default_actions": [
        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
      ]
    }
  }
}
```

```json
{
  "domain_id": "repo_handoff",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "handoff_if_truth_or_mirror_scope:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md",
      "handoff_if_deeper_app_contract_exists"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": []
  }
}
```
</part_B>
