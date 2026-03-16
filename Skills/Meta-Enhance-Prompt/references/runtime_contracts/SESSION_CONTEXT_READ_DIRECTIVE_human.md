---
doc_id: meta_enhance_prompt.runtime.session_context_read_directive
doc_type: topic_atom
topic: Session context read workflow mirror for Meta-Enhance-Prompt
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This human mirror documents the session context pre-read workflow routed from the facade.
---

# SESSION_CONTEXT_READ_DIRECTIVE

<part_A>
- 本分支负责按 `codex id / session id / resume id` 或其他 rollout 键快速锚定目标会话，并提取默认聚焦的 `user prompt + assistant reply`。
- 当用户先要求“阅读聊天记录/最后一轮 assistant reply”时，应先走这个 CLI，再继续做 `intent_clarify`、分析或回答。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_session_context_read_workflow",
  "directive_version": "3.2.0",
  "doc_kind": "workflow",
  "topic": "session-context-read",
  "purpose": "Locate a target rollout by codex/session/resume id or another rollout key, then return the focused user prompt plus assistant reply needed for Meta-Enhance-Prompt pre-read context.",
  "instruction": [
    "Use scripts/Cli_Toolbox.py read-session-context --lookup-key <rollout_key> --lookup-id <id> --json as the default cross-session chat read entry.",
    "Prefer the direct aliases --codex-id / --session-id / --resume-id when the caller already provides one of those ids.",
    "When the user explicitly asks to read chat history first, run this CLI before intent clarification, analysis, or answer drafting.",
    "Keep the default scope on the paired user prompt and assistant reply, and only expand context_mode or message filters when the downstream task truly needs more context.",
    "Reuse message-role, message-key, message-query, and context-mode parameters to inspect other context from the same matched session without hand-searching jsonl files."
  ],
  "workflow": [
    "Resolve the target rollout by --lookup-key + --lookup-id or the direct codex/session/resume id aliases.",
    "If no message selector is provided, select the latest assistant message inside the matched session.",
    "Return the nearest paired user prompt together with that assistant reply as focused_chat.",
    "When extra context is needed, rerun the same command with message filters or a wider context-mode such as window/all.",
    "Feed the returned focused_chat payload into the downstream intent clarification, analysis, or answer step."
  ],
  "rules": [
    "Do not manually grep or hand-read raw session jsonl files when this CLI can anchor the rollout directly.",
    "Do not treat the lookup id or the sentence that asks for history reading as part of the prompt that should be strengthened.",
    "Do not expand to the full session transcript by default; user prompt plus assistant reply is the default output scope."
  ]
}
```
</part_B>
