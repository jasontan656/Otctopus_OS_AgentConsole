---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
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
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Client_Applications` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Dev-VUE3-WebUI-Frontend (frontend governance baseline for Client_Applications)",
    "$Meta-RootFile-Manager (AGENTS governance mapping flow)"
  ],
  "turn_start_actions": [
    "load the returned target-contract JSON before following Client_Applications local runtime rules",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the task enters frontend development under Client_Applications, use the active frontend governance standard",
    "if the task governs this AGENTS.md, use the governed collect/push flow instead of directly editing the external file"
  ],
  "runtime_constraints": [
    "Client_Applications frontend work must follow the active frontend governance standard",
    "this AGENTS.md is governed and must not be directly edited as an external file",
    "treat CLI JSON as the primary runtime rule source"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect or answer without changing Client_Applications files",
      "default_actions": [
        "prefer the target-contract JSON as the primary runtime entry",
        "load the active frontend governance only when the task enters actual frontend work"
      ]
    },
    "WRITE_EXEC": {
      "goal": "change Client_Applications artifacts under governed frontend rules",
      "default_actions": [
        "use the active frontend governance as the mandatory development standard",
        "when governing this AGENTS.md, finish the collect/push loop"
      ]
    }
  },
  "repo_local_contract_handoff": [
    "for frontend development under Client_Applications, load and follow the active frontend governance before editing",
    "for AGENTS governance, keep the internal managed pair and the external AGENTS.md synchronized through the governed mapping flow"
  ],
  "forbidden_primary_runtime_pattern": [
    "Do not perform Client_Applications frontend work while ignoring the active frontend governance.",
    "Do not directly edit the external Client_Applications/AGENTS.md outside the governed mapping flow."
  ],
  "turn_end_actions": [
    "if the turn changed Client_Applications frontend artifacts, confirm the active frontend governance was used as the governing standard",
    "if the turn governed this AGENTS.md, complete the governed collect/push loop before closing"
  ],
  "repo_name": "Octopus_OS"
}
```
</part_B>
