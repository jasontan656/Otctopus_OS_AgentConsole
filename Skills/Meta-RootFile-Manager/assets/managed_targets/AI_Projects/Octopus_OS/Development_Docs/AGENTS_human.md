---
owner: "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 当前可用的 skills backend Python 虚拟环境为：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills`。
- 运行 skills CLI 时，优先使用：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3`。
- 若需要运行 `pytest` 验证 skills 或 backend Python 相关改动，也优先使用同一虚拟环境，例如：`<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 -m pytest`。
- 在处理当前开发文档容器规则之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/AGENTS.md" --json`

2. 当前受管容器
- 当前受管容器：`Octopus_OS/Development_Docs`。
- 当前 mother_doc 真源根：`/home/jasontan656/AI_Projects/Octopus_OS/Development_Docs/mother_doc`。
- 当前前端镜像根：`/home/jasontan656/AI_Projects/Octopus_OS/Client_Applications/mother_doc`。

3. 当前治理占位
- Mother_doc changes must happen here。
- Client mirror sync target：`Octopus_OS/Client_Applications/mother_doc`。
- After mother_doc writes here, run the local development workflow turn hook to refresh the client mirror copy。
</part_A>

<part_B>

```json
{
  "owner": "由 `$Meta-RootFile-Manager` 作为 `Octopus_OS/Development_Docs` container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。",
  "entry_role": "devflow_module_docs_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Workflow-MotherDoc-OctopusOS (mother_doc writeback and client mirror sync)",
    "$Workflow-ConstructionPlan-OctopusOS (execution pack planning)",
    "$Workflow-Implementation-OctopusOS (active pack implementation)",
    "$Workflow-Acceptance-OctopusOS (delivery closeout and witness)",
    "$Meta-RootFile-Manager (AGENTS governance mapping flow)"
  ],
  "turn_start_actions": [],
  "runtime_constraints": [
    "Mother_doc changes must happen here before any client mirror refresh."
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "inspect or answer within Development_Docs without editing files",
      "default_actions": [
        "load extra workflow documents only when this container task needs them"
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
    "Use the local development workflow runtime for mother_doc work, then refresh the client mirror copy."
  ],
  "forbidden_primary_runtime_pattern": [],
  "turn_end_actions": [
    "If this turn changed mother_doc here, refresh the client mirror copy before closing the turn."
  ]
}
```
</part_B>
