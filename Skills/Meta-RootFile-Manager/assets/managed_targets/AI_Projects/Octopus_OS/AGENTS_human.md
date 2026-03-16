---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects/Octopus_OS` 的仓库根运行时合同。
- 本层只做 repo 根路由，不重复 `Development_Docs` 与 `Client_Applications` 已各自承接的更窄规则。

2. 一级读取入口
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --json`

3. 二级分域读取
- hook_identity:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- 若任务发生 `Octopus_OS` repo write，同回合追加 `Meta-github-operation`，并在收口前完成同回合 Git traceability。
- 若任务改动仓库级结构、容器边界、对象定位、folder planning 或跨对象结构关系，继续读取 `Dev-ProjectStructure-Constitution`。
- 若任务改动 backend-side Python code、backend runtime glue、repo-level Python tooling 或其他非前端 Python 资产，继续读取 `Dev-PythonCode-Constitution`。
- 若任务治理当前 repo 的 `AGENTS.md` 或其他 repo root 受管 root files，必须通过 `Meta-RootFile-Manager` 的 internal truth -> centered push -> lint 主链完成；`collect` 只保留 reverse-sync / recovery。
- 若任务落到 `mother_doc` 真源、workflow contract、文档结构或 client mirror 同步语义，下一站是 `/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md`。
- 若任务落到面向最终用户的界面、交互、页面结构或 client surface，下一站是 `/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md`。
</contract>

<reminder>
1. 环境提醒
- workspace root 已承接通用 Python 环境与 skills CLI 启动说明，这里不重复展开。

2. 协作提醒
- repo 根只负责路由；进入更窄容器后，优先遵循更窄合同。
</reminder>
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "octopus_os_repo_root_contract",
    "contract_scope": "repo_root",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "read_target_contract:/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md",
      "plan_same_turn_git_traceability_if_repo_write_scope"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "repo_writes_require_same_turn_git_traceability",
      "structure_governance_handoff:Dev-ProjectStructure-Constitution",
      "backend_python_governance_handoff:Dev-PythonCode-Constitution",
      "agents_governance_uses_meta_rootfile_manager_centered_push",
      "route_devflow_work_to:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md",
      "route_client_surface_work_to:/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_or_route_within_octopus_os",
      "default_actions": [
        "read_structure_contract_when_repo_structure_scope",
        "read_python_contract_when_backend_python_scope",
        "handoff_when_child_contract_is_more_specific"
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
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "handoff_repo_structure_scope_to_dev_projectstructure_constitution",
      "handoff_backend_python_scope_to_dev_pythoncode_constitution",
      "handoff_repo_rootfile_governance_to_meta_rootfile_manager_centered_push",
      "handoff_if_mother_doc_or_client_mirror:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md",
      "handoff_if_client_surface:/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": [
      "complete_octopus_os_git_traceability_if_repo_writes_occur",
      "complete_rootfile_centered_push_and_lint_if_repo_rootfile_changed"
    ]
  }
}
```
</part_B>
