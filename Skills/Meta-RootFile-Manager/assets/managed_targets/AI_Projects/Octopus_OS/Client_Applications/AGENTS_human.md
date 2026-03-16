---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 当前可用的 skills backend Python 虚拟环境为：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills`。
- 运行 skills CLI 时，优先使用：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3`。
- 若需要运行 `pytest` 验证 skills 或 backend Python 相关改动，也优先使用同一虚拟环境，例如：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 -m pytest`。
- 在读取 `Octopus_OS/Client_Applications` 容器 contract 前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --json`

2. 当前容器定位
- `Client_Applications` 承载面向最终用户的 client application surfaces。
- 用户后续应补全该容器的前端与交互治理内容。
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Workflow-CentralFlow1-OctopusOS (this skill drives the development here and is responsible for mother doc edits.)",
    "$Meta-RootFile-Manager (AGENTS governance mapping flow)"
  ],
  "turn_start_actions": [],
  "runtime_constraints": [],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect Client_Applications frontend surfaces without mutating tracked files",
      "default_actions": []
    },
    "WRITE_EXEC": {
      "goal": "default to full-coverage edits for the intended change",
      "default_actions": [
        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
      ]
    }
  },
  "repo_local_contract_handoff": [
    "when another governed sub-container becomes active, load its local contract before following sub-container-specific rules"
  ],
  "forbidden_primary_runtime_pattern": [],
  "turn_end_actions": [],
  "repo_name": "Octopus_OS"
}
```
</part_B>
