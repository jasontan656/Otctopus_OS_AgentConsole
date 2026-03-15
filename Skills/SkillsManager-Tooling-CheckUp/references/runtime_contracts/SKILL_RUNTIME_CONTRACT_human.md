---
doc_id: skillsmanager_tooling_checkup.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: SKILL_RUNTIME_CONTRACT
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# SKILL_RUNTIME_CONTRACT

<part_A>
- 人类阅读入口：本文件说明 `SkillsManager-Tooling-CheckUp` 使用 CLI-first runtime contract。
- 模型运行时入口固定为：
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic <topic> --json`
- `govern-target` 只负责目标 skill 的 tooling surface 审计，不承担目标技能形态治理。
- 人类可以阅读本 markdown 的叙事部分，但模型应总是优先消费 Part B 的 JSON payload。
</part_A>

<part_B>

```json
{
  "contract_name": "skills_tooling_checkup_runtime_contract",
  "contract_version": "2.4.0",
  "skill_name": "SkillsManager-Tooling-CheckUp",
  "runtime_source_policy": {
    "primary_runtime_source": "CLI_JSON",
    "human_markdown_role": "part_a_narrative_for_humans",
    "payload_role": "part_b_json_for_models",
    "markdown_is_not_primary_instruction_source": true
  },
  "tool_entry": {
    "script": "scripts/Cli_Toolbox.py",
    "commands": {
      "contract": "./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py contract --json",
      "directive": "./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py directive --topic <topic> --json",
      "govern-target": "./.venv_backend_skills/bin/python Skills/SkillsManager-Tooling-CheckUp/scripts/Cli_Toolbox.py govern-target --target-skill-root <path> --json"
    }
  },
  "must_use_sequence": [
    "Call contract before consuming runtime guidance for this skill.",
    "Choose the directive topic by actual task intent.",
    "Treat returned JSON payloads as the primary instruction source.",
    "Open human markdown mirrors or legacy reference docs only when the direct JSON payload leaves a real gap."
  ],
  "directive_topics": [
    {
      "topic": "read-audit",
      "doc_kind": "instruction",
      "use_when": "The task is read-only diagnosis, evidence collection, or semantic classification."
    },
    {
      "topic": "remediation",
      "doc_kind": "workflow",
      "use_when": "The task will edit target skill tooling code or target skill governance assets."
    },
    {
      "topic": "output-governance",
      "doc_kind": "contract",
      "use_when": "The task mentions runtime logs, audit files, default outputs, directed outputs, or migration duties."
    },
    {
      "topic": "cli-surface",
      "doc_kind": "contract",
      "use_when": "The task audits command naming, argument contract, JSON output shape, error shape, or explicit CLI entry expectations."
    },
    {
      "topic": "tooling-boundary",
      "doc_kind": "guide",
      "use_when": "The task needs parser/schema/helper/lint/test/glue responsibility boundaries or must distinguish tooling from domain policy."
    },
    {
      "topic": "techstack-baseline",
      "doc_kind": "guide",
      "use_when": "The task must decide whether existing repo-local dependencies already cover the needed capability."
    },
    {
      "topic": "tooling-entry",
      "doc_kind": "guide",
      "use_when": "The task needs the local toolbox surface, command examples, or human/model boundary guidance."
    }
  ],
  "hard_constraints": [
    "Do not treat markdown path chains as the main runtime instructions.",
    "Do not output path metadata instead of direct action guidance.",
    "Do not invent a parallel governance flow when the directive payload already answers the active question.",
    "Do not use this skill to govern target skill root shape, SKILL.md facade shape, path chain shape, or anchor graph shape.",
    "Do not edit the codex installed copy directly; edit the mirror copy and sync downstream after validation."
  ],
  "target_skill_handoff": [
    "After this skill clarifies the review or remediation workflow, enter the target skill through its own governed workflow and local execution commands.",
    "Use the target skill's existing tests and lint commands for behavior verification.",
    "If Python files are edited, run Dev-PythonCode-Constitution lint on the concrete Python target scope before closing the turn.",
    "Use govern-target only for tooling surface audits: scripts surface, explicit CLI entry, dependency-baseline drift, and output governance.",
    "Delegate Python or TypeScript language-style rules, fat-file policy, and language-specific lint baselines to the relevant language constitution instead of restating them here."
  ]
}
```
</part_B>
