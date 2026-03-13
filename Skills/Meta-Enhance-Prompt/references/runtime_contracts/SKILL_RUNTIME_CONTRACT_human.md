---
doc_id: "meta_enhance_prompt.runtime.skill_runtime_contract"
doc_type: "topic_atom"
topic: "CLI-first runtime contract for Meta-Enhance-Prompt"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This human mirror implements the runtime contract promised by the skill facade."
---

# SKILL_RUNTIME_CONTRACT

<part_A>
- 人类阅读入口：`Meta-Enhance-Prompt` 已切换为 CLI-first runtime contract。
- 模型必须先调用：
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py contract --json`
  - `./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py directive --topic <topic> --json`
- `filter_active_invoke_output.py` 负责最终限形与受管输出治理；它不替代 repo 调研。
</part_A>

<part_B>

```json
{
  "contract_name": "meta_enhance_prompt_runtime_contract",
  "contract_version": "2.0.0",
  "skill_name": "Meta-Enhance-Prompt",
  "runtime_source_policy": {
    "primary_runtime_source": "CLI_JSON",
    "human_markdown_role": "part_a_narrative_for_humans",
    "payload_role": "part_b_json_for_models",
    "markdown_is_not_primary_instruction_source": true
  },
  "tool_entry": {
    "script": "scripts/Cli_Toolbox.py",
    "commands": {
      "contract": "./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py contract --json",
      "directive": "./.venv_backend_skills/bin/python Skills/Meta-Enhance-Prompt/scripts/Cli_Toolbox.py directive --topic <topic> --json",
      "active_invoke": "python3 Skills/Meta-Enhance-Prompt/scripts/filter_active_invoke_output.py --mode active_invoke --input-text \"<RAW_PROMPT_OUTPUT>\" --json",
      "skill_directive": "python3 Skills/Meta-Enhance-Prompt/scripts/filter_active_invoke_output.py --mode skill_directive --input-text \"<USER_INTENT_TEXT>\" --json"
    }
  },
  "must_use_sequence": [
    "Call contract before consuming runtime guidance for this skill.",
    "Choose the directive topic by actual task intent.",
    "Treat returned JSON payloads as the primary instruction source.",
    "Do the repo survey before invoking active_invoke.",
    "Publish only the filtered final output, not the raw prompt draft."
  ],
  "directive_topics": [
    {
      "topic": "active-invoke",
      "doc_kind": "workflow",
      "use_when": "The task needs the fixed six-section prompt output."
    },
    {
      "topic": "skill-directive",
      "doc_kind": "instruction",
      "use_when": "The task needs the CLI-first runtime entry instead of reading SKILL.md."
    },
    {
      "topic": "output-governance",
      "doc_kind": "contract",
      "use_when": "The task mentions runtime logs, result paths, default output locations, or migration duties."
    }
  ],
  "hard_constraints": [
    "Do not treat SKILL.md or legacy markdown docs as the primary runtime instruction source.",
    "Do not auto-fill missing contract sections with placeholder defaults.",
    "Do not publish a final prompt when required sections are missing.",
    "Do not emit only path pointers when the runtime needs direct CLI guidance."
  ],
  "runtime_output_policy": {
    "runtime_log_policy": "Append machine and human logs under the governed runtime root for each run.",
    "result_policy": "Write the emitted result to an explicit output path when provided, otherwise default under the governed result root.",
    "default_runtime_root": "Codex_Skill_Runtime/Meta-Enhance-Prompt",
    "default_result_root": "Codex_Skills_Result/Meta-Enhance-Prompt"
  }
}
```
</part_B>
