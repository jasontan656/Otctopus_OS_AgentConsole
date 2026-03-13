---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理当前目录路径规则之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md" --json`

2. 待治理骨架
- 该目录已进入治理范围。
- 用户后续应补全该目录所需的具体治理内容。

3. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
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
    "$Dev-OctopusOS-Constitution-ProjectStructure (Octopus_OS structure governance)",
    "$Dev-PythonCode-Constitution (non-frontend Python governance)",
    "$Meta-RootFile-Manager (AGENTS governance mapping flow)"
  ],
  "turn_start_actions": [
    "load the returned target-contract JSON before following Octopus_OS local runtime rules",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the turn is not read-only, plan same-turn Git traceability from the start",
    "if the task changes Octopus_OS structure, route through the active structure governance before editing",
    "if the task changes Python code outside frontend work, route through the active Python governance before editing",
    "if the task governs this AGENTS.md, use the governed collect/push flow instead of directly editing the external file"
  ],
  "runtime_constraints": [
    "any non-read-only change in Octopus_OS must leave same-turn Git traceability",
    "Octopus_OS structure governance must keep artifact shape plus structure-side descriptions or registrations bidirectionally synchronized",
    "all non-frontend code work must obey the active Python governance for this repo",
    "this AGENTS.md is governed and must not be directly edited as an external file",
    "treat CLI JSON as the primary runtime rule source"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect or answer without changing Octopus_OS files",
      "default_actions": [
        "prefer the target-contract JSON as the primary runtime entry",
        "read additional structure or Python rules only when the concrete task requires them"
      ]
    },
    "WRITE_EXEC": {
      "goal": "change Octopus_OS artifacts under governed runtime rules",
      "default_actions": [
        "complete same-turn commit-and-push traceability when Octopus_OS is written",
        "keep structure-level changes synchronized with product artifacts plus structure-side registrations",
        "apply the repo's non-frontend Python governance before Python edits",
        "when governing this AGENTS.md, finish the collect/push loop"
      ]
    }
  },
  "repo_local_contract_handoff": [
    "for structure-level planning, load the current structure governance contract before editing",
    "for Python code work outside frontend, load the current Python governance contract before editing",
    "for AGENTS governance, keep the internal managed pair and the external AGENTS.md synchronized through the governed mapping flow"
  ],
  "forbidden_primary_runtime_pattern": [
    "Do not directly edit the external Octopus_OS/AGENTS.md without going through Meta-RootFile-Manager.",
    "Do not perform write changes in Octopus_OS without same-turn Git traceability.",
    "Do not change Octopus_OS structure while leaving the project-structure skill descriptions or registrations stale."
  ],
  "turn_end_actions": [
    "if the turn changed Octopus_OS, complete same-turn commit-and-push traceability",
    "if the turn changed Octopus_OS structure, confirm the product artifact shape and the structure-side descriptions or registrations were updated together",
    "if the turn governed this AGENTS.md, complete the governed collect/push loop before closing"
  ],
  "repo_name": "Octopus_OS"
}
```
</part_B>
