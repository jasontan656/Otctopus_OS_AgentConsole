---
doc_id: meta_enhance_prompt.runtime.skill_directive_instruction
doc_type: topic_atom
topic: Skill directive mirror for Meta-Enhance-Prompt runtime entry
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This human mirror documents the CLI-first runtime entry routed from the facade.
---

# SKILL_DIRECTIVE_DIRECTIVE

<part_A>
- 本分支用于给运行时提供 CLI-first 入口，不再回退到 `SKILL.md` 路径链。
- 若需要真实合同内容，应继续调用 `Cli_Toolbox.py` 的 `contract` 或 `directive` 子命令。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_skill_directive_instruction",
  "directive_version": "2.0.0",
  "doc_kind": "instruction",
  "topic": "skill-directive",
  "purpose": "Return the CLI-first runtime entry for Meta-Enhance-Prompt instead of routing callers back to SKILL.md.",
  "instruction": [
    "Start from scripts/Cli_Toolbox.py contract --json.",
    "Use scripts/Cli_Toolbox.py directive --topic active-invoke --json when the caller needs the six-section filter workflow.",
    "Use scripts/Cli_Toolbox.py directive --topic output-governance --json when the caller needs runtime/result path policy."
  ],
  "workflow": [
    "Resolve the Meta-Enhance-Prompt toolbox path.",
    "Return CLI commands and direct runtime payload references instead of markdown file paths.",
    "Keep the answer focused on runtime entry and next command."
  ],
  "rules": [
    "Do not tell the model to read SKILL.md as the primary runtime instruction.",
    "Do not emit only file path metadata when the runtime needs executable CLI entry points."
  ]
}
```
</part_B>
