---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在读取 `Octopus_OS` repo 级 runtime contract 前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --json`

2. 当前治理占位
- 当前受管容器：`Octopus_OS`。
- 用户后续应补全该 repo 根的专属治理内容。
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$meta-github-operation (Git traceability for Octopus_OS writes)",
    "$Dev-ProjectStructure-Constitution (Octopus_OS structure governance)",
    "$Dev-PythonCode-Constitution (non-frontend Python governance)",
    "$Meta-RootFile-Manager (AGENTS governance mapping flow)"
  ],
  "turn_start_actions": [],
  "runtime_constraints": [],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect or answer without changing Octopus_OS files",
      "default_actions": [
        "read additional structure or Python rules only when the concrete task requires them"
      ]
    },
    "WRITE_EXEC": {
      "goal": "default to full-coverage edits for the intended change",
      "default_actions": [
        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
      ]
    }
  },
  "repo_local_contract_handoff": [],
  "forbidden_primary_runtime_pattern": [],
  "turn_end_actions": [],
  "repo_name": "Octopus_OS"
}
```
</part_B>
