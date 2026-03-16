---
owner: "由 `$Meta-RootFile-Manager` 作为 `.codex/skills` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects/.codex/skills` 安装侧容器的运行时合同。
- 安装侧适合读取与核对；长期写入真源仍位于 `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills`。

2. 一级读取入口
- `MDM_WORKSPACE_ROOT=<codex_home_parent> <root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-maintain --intent "<natural language request>" --json`

3. 二级分域读取
- hook_identity:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- 若安装侧与产品仓真源同时可见，以产品仓结果为最终裁决。
- 安装侧写入由 mirror/install 主链触发，不在安装侧直接扩写技能真源语义。
</contract>

<reminder>
1. 环境提醒
- 语言边界沿用 workspace root 的约定。
- 这里是 symbolic target，命令中的 `MDM_WORKSPACE_ROOT` 需要指向受管工作区根。

2. 协作提醒
- 安装侧更适合作为读取与校验对象。
- 技能长期真源与结构升级仍回到 `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills` 完成。
</reminder>
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "codex_skills_installation_contract",
    "contract_scope": "installation_container",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "run_agents_maintain_entry_for_codex_skills_requests",
      "classify_turn_mode:READ_EXEC|WRITE_EXEC"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "skills_truth_source:/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills",
      "codex_installation_is_mirror_only"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_codex_skills_installation_without_mutation",
      "default_actions": [
        "read_installation_entry_before_local_checks"
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
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "route_skill_writes_back_to_repo_truth_source",
      "verify_installation_after_repo_push"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "MDM_WORKSPACE_ROOT=/home/jasontan656/AI_Projects /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/.codex/skills/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": []
  }
}
```
</part_B>
