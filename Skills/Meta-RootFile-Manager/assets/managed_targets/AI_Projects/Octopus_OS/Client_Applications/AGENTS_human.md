[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前目录路径规则之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/AGENTS.md" --json`

2. 待治理骨架
- 该目录已进入治理范围。
- 用户后续应补全该目录所需的具体治理内容。

3. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>

<part_B>

```json
{
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Dev-VUE3-WebUI-Frontend (the mandatory frontend development constitution for Client_Applications; do not violate it)",
    "$Meta-RootFile-Manager (required whenever governing this AGENTS.md; do not directly edit the external AGENTS.md)"
  ],
  "turn_start_actions": [
    "load the returned target-contract JSON before following Client_Applications local runtime rules",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the task enters frontend development under Client_Applications, use $Dev-VUE3-WebUI-Frontend as the governing frontend standard",
    "if the task governs this AGENTS.md, use $Meta-RootFile-Manager collect/push flow instead of directly editing the external file"
  ],
  "runtime_constraints": [
    "Client_Applications frontend work must use $Dev-VUE3-WebUI-Frontend as the governing frontend standard and must not violate it",
    "this AGENTS.md is governed by $Meta-RootFile-Manager and must not be directly edited as an external file",
    "treat CLI JSON as the primary runtime rule source"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect or answer without changing Client_Applications files",
      "default_actions": [
        "prefer the target-contract JSON as the primary runtime entry",
        "read Dev-VUE3-WebUI-Frontend only when the task enters actual frontend work"
      ]
    },
    "WRITE_EXEC": {
      "goal": "change Client_Applications artifacts under governed frontend rules",
      "default_actions": [
        "use $Dev-VUE3-WebUI-Frontend as the mandatory frontend development standard",
        "use $Meta-RootFile-Manager when governing this AGENTS.md and finish the collect/push loop"
      ]
    }
  },
  "repo_local_contract_handoff": [
    "for frontend development under Client_Applications, read and follow Dev-VUE3-WebUI-Frontend before editing",
    "for AGENTS governance, keep the internal managed pair and the external AGENTS.md synchronized through Meta-RootFile-Manager"
  ],
  "forbidden_primary_runtime_pattern": [
    "Do not perform Client_Applications frontend work while ignoring Dev-VUE3-WebUI-Frontend.",
    "Do not directly edit the external Client_Applications/AGENTS.md without going through Meta-RootFile-Manager."
  ],
  "turn_end_actions": [
    "if the turn changed Client_Applications frontend artifacts, confirm Dev-VUE3-WebUI-Frontend was used as the governing standard",
    "if the turn governed this AGENTS.md, complete the Meta-RootFile-Manager collect/push loop before closing"
  ],
  "repo_name": "Octopus_OS"
}
```
</part_B>
