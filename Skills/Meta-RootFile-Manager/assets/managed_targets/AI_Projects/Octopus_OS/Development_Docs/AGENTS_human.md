---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs` 的文档真源合同。
- 本层负责 `mother_doc` 真源、workflow 路由、client mirror 触发条件与同步完成定义。

2. 一级读取入口
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --json`

3. 二级分域读取
- hook_identity:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- `mother_doc` 真源根是 `/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/mother_doc`；client mirror 根是 `/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/mother_doc`。
- 当任务修改 `mother_doc` 真源、文档结构、章节路由或架构语义时，继续读取 `$Workflow-MotherDoc-OctopusOS`。
- 当任务把已确认需求拆成 execution packs 时，继续读取 `$Workflow-ConstructionPlan-OctopusOS`。
- 当任务消费 active pack 落实现与证据时，继续读取 `$Workflow-Implementation-OctopusOS`。
- 当任务进入真实 bring-up、witness 或交付收口时，继续读取 `$Workflow-Acceptance-OctopusOS`。
- 触发 client mirror 刷新的条件是：本回合改动了 `mother_doc` 真源内容，或改动了会影响 client mirror 的文档路由、章节语义。
- 本层完成定义是：`/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/mother_doc` 已更新，且 `/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/mother_doc` 已按同一语义刷新，不留陈旧差异。
</contract>

<reminder>
1. 环境提醒
- workspace root 与 `Octopus_OS` repo root 已承接通用环境说明，这里只保留文档真源约束。

2. 协作提醒
- workflow 只按当前阶段读取，不在一个回合里平铺全部 workflow 语义。
- client mirror 只承接镜像，不替代 `Development_Docs/mother_doc` 真源。
</reminder>
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "octopus_os_development_docs_contract",
    "contract_scope": "container",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "read_target_contract:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md",
      "classify_devflow_stage:mother_doc|construction_plan|implementation|acceptance"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "mother_doc_truth_root:/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/mother_doc",
      "client_mirror_root:/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/mother_doc",
      "write_truth_before_mirror_refresh"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_development_docs_without_file_mutation",
      "default_actions": [
        "read_selected_workflow_contract_only_when_stage_is_known"
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
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "select_stage_specific_contract_before_write",
      "route_truth_and_mirror_decisions_inside_development_docs"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": [
      "refresh_client_mirror_when_truth_or_route_changed"
    ]
  }
}
```
</part_B>
