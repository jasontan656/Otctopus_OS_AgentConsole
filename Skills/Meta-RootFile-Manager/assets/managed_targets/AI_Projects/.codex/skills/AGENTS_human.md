---
owner: "由 `$Meta-RootFile-Manager` 作为 `.codex/skills` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- `MDM_WORKSPACE_ROOT=<codex_home_parent> <root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-maintain --intent "<natural language request>" --json`

2. 技能类任务附加入口
- N/A

3. 语言规范
- N/A

4. 当前受管 repo 边界
- 禁止直接在 `<codex_home>/skills` 安装目录修改技能。

5. Multi-AGENT 工作模式
- N/A

6. 治理链约束
- N/A
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `.codex/skills` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "codex_skills_installation_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "N/A"
  ],
  "turn_start_actions": [
    "run the agents-maintain CLI for AGENTS maintenance requests first"
  ],
  "runtime_constraints": [
    "do not modify skills directly under <codex_home>/skills"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "obtain the payload contract for the codex skills installation entry before inspection",
      "default_actions": [
        "N/A"
      ]
    },
    "WRITE_EXEC": {
      "goal": "default to full-coverage edits for the intended change",
      "default_actions": [
        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
      ]
    }
  },
  "repo_local_contract_handoff": [
    "use the agents-maintain placement result for this target before local processing"
  ],
  "forbidden_primary_runtime_pattern": [
    "direct skill edits under <codex_home>/skills"
  ],
  "turn_end_actions": [
    "N/A"
  ]
}
```
</part_B>
