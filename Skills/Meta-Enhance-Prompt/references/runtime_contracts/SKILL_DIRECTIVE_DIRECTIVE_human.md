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
- 若用户给出 `codex/session/resume id` 并要求先读聊天记录，本分支应先下发 `session-context-read` 与 `read-session-context` 命令，而不是让助理手工搜会话文件。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_skill_directive_instruction",
  "directive_version": "3.2.0",
  "doc_kind": "instruction",
  "topic": "skill-directive",
  "purpose": "Return the CLI-first runtime entry for Meta-Enhance-Prompt instead of routing callers back to SKILL.md.",
  "instruction": [
    "Start from scripts/Cli_Toolbox.py contract --json.",
    "If the caller provides codex id/session id/resume id and asks to read chat history first, use scripts/Cli_Toolbox.py directive --topic session-context-read --json and then call scripts/Cli_Toolbox.py read-session-context before any further reasoning.",
    "Use scripts/Cli_Toolbox.py directive --topic intent-clarify --json when the caller needs the canonical intent clarification workflow.",
    "Treat scripts/Cli_Toolbox.py directive --topic active-invoke --json as a legacy alias only.",
    "If the caller provides codex id/session id/resume id, treat it as pre-read conversation context rather than as the prompt body to strengthen.",
    "Use scripts/Cli_Toolbox.py directive --topic output-governance --json when the caller needs runtime/result path policy."
  ],
  "workflow": [
    "Resolve the Meta-Enhance-Prompt toolbox path.",
    "When session ids are present, return the session-context-read directive plus a ready-to-run read-session-context command before the intent workflow.",
    "Return CLI commands and direct runtime payload references instead of markdown file paths.",
    "Keep the answer focused on runtime entry and next command."
  ],
  "rules": [
    "Do not tell the model to read SKILL.md as the primary runtime instruction.",
    "Do not skip the dedicated chat-history CLI and fall back to hand-search when the user explicitly asked to read session history first.",
    "Do not emit only file path metadata when the runtime needs executable CLI entry points."
  ]
}
```
</part_B>
