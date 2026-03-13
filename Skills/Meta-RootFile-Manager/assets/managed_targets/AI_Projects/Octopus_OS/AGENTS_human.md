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
    "classify the turn as READ_EXEC or WRITE_EXEC"
  ],
  "runtime_constraints": [
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
        "edit the minimal correct scope that matches the user intent"
      ]
    }
  },
  "repo_local_contract_handoff": [
    "when another governed sub-container becomes active, load its local contract before following sub-container-specific rules"
  ],
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not bypass the returned target-contract JSON when local runtime rules are required."
  ],
  "turn_end_actions": [],
  "repo_name": "Octopus_OS"
}
```
</part_B>
