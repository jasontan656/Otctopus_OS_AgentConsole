---
doc_id: functional_humenworkzone_manager.runtime_contract
doc_type: topic_atom
topic: CLI-first runtime contract for Functional-HumenWorkZone-Manager
node_role: topic_atom
domain_type: runtime_contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The runtime contract is the first governed runtime branch linked from the facade.
- target: TASK_ROUTING_GUIDE_human.md
  relation: routes_to
  direction: downstream
  reason: Runtime branch selection follows the task-routing directive.
- target: EXECUTION_BOUNDARY_CONTRACT_human.md
  relation: routes_to
  direction: downstream
  reason: File operations must follow the execution-boundary directive.
---

# SKILL_RUNTIME_CONTRACT

<part_A>
- 人类阅读时可用本文件理解 `Functional-HumenWorkZone-Manager` 的 CLI-first 入口。
- 本技能当前通过 `contract / directive / paths` 三个命令输出运行时合同，而不是让模型从 markdown 路径链自行摸索。
- 当任务进入具体分支判断或文件操作边界时，再读取对应 directive。
</part_A>

<part_B>

```json
{
  "contract_name": "functional_humenworkzone_manager_runtime_contract",
  "contract_version": "1.0.0",
  "skill_name": "Functional-HumenWorkZone-Manager",
  "runtime_source_policy": {
    "primary_runtime_source": "CLI_JSON",
    "human_markdown_role": "part_a_narrative_for_humans",
    "payload_role": "part_b_json_for_models",
    "markdown_is_not_primary_instruction_source": true
  },
  "tool_entry": {
    "script": "scripts/Cli_Toolbox.py",
    "commands": {
      "contract": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json",
      "directive": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic <topic> --json",
      "paths": "./.venv_backend_skills/bin/python Skills/Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json"
    }
  },
  "must_use_sequence": [
    "Call contract --json before consuming runtime guidance for this skill.",
    "Read directive --topic task-routing --json to choose the correct Human_Work_Zone management branch.",
    "Read directive --topic execution-boundary --json before moving, renaming, or deleting files.",
    "Call paths --json when you need the canonical managed root or any managed zone path.",
    "Open legacy markdown routing and runtime docs only after the CLI JSON payload points to the relevant branch."
  ],
  "directive_topics": [
    {
      "topic": "task-routing",
      "doc_kind": "guide",
      "use_when": "Use this first to map the user request into the correct Human_Work_Zone management branch."
    },
    {
      "topic": "execution-boundary",
      "doc_kind": "contract",
      "use_when": "Use this before file operations to keep scope locked to Human_Work_Zone and its managed zones."
    }
  ],
  "managed_root": "/home/jasontan656/AI_Projects/Human_Work_Zone",
  "hard_constraints": [
    "Treat CLI JSON as the primary runtime source; SKILL.md remains a facade only.",
    "Keep all write actions scoped to Human_Work_Zone unless the user explicitly points to an external source folder for intake.",
    "Route open-source projects, backups, project analysis, books, temporary projects, temporary governance files, company documents, and external research reports into their dedicated managed zones.",
    "When intake changes names or locations, update the corresponding README inventory in the same turn."
  ]
}
```
</part_B>
