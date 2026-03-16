---
doc_id: meta_enhance_prompt.runtime.intent_clarify_directive
doc_type: topic_atom
topic: Intent clarify workflow mirror for Meta-Enhance-Prompt
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This human mirror documents the intent clarification workflow routed from the facade.
---

# INTENT_CLARIFY_DIRECTIVE

<part_A>
- 本分支只负责把用户原话或意图草稿限形成最终单段 `INTENT:` 输出。
- 若请求里先要求“读 `codex/session/resume id` 聊天记录”，必须先调用 `read-session-context`，再决定最终 `INTENT:`。
- `intent_clarify` 不允许再扩写成六段合同；`active_invoke` 只保留为兼容别名。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_intent_clarify_workflow",
  "directive_version": "3.2.0",
  "doc_kind": "workflow",
  "topic": "intent-clarify",
  "purpose": "Clarify the user's real need into a single reusable INTENT block and drop nonessential prompt scaffolding.",
  "instruction": [
    "Build or receive a raw draft that already expresses the clarified user intent, either as an INTENT block or a pure intent paragraph.",
    "If the caller provides codex id/session id/resume id, treat it as a context lookup parameter. Read the referenced conversation context first with read-session-context, but do not let that lookup instruction become part of the strengthened prompt.",
    "When the request uses a wrapper such as `先阅读 codex id: xxxx ... 帮我强化如下prompt:(...)`, keep only the inner target prompt as the enhancement target.",
    "Filter the draft into exactly one final INTENT section without appending GOAL, REPO_CONTEXT_AND_IMPACT, INPUTS, OUTPUTS, BOUNDARIES, or VALIDATION.",
    "Reject blank or unusable intent content instead of inventing filler.",
    "When the final INTENT block is later published in chat, do not prepend another paraphrase that repeats the same intent."
  ],
  "workflow": [
    "Read the raw user prompt or the raw intent draft produced for this skill.",
    "If codex/session/resume id is present, run scripts/Cli_Toolbox.py read-session-context first and use focused_chat.user_prompt plus focused_chat.assistant_reply as the default pre-read context before deciding the strengthened intent.",
    "Run scripts/filter_active_invoke_output.py --mode intent_clarify.",
    "Treat scripts/filter_active_invoke_output.py --mode active_invoke as a legacy alias only.",
    "Write runtime logs under the governed runtime root and write the pure INTENT output to the explicit output path or governed result root.",
    "Publish the filtered final output only if validation succeeds."
  ],
  "rules": [
    "Do not claim repo survey is mandatory for this skill unless the downstream task truly depends on repo evidence.",
    "Do not include codex/session/resume id lookup commands, cross-session reading instructions, or wrapper verbs such as `先阅读` / `帮我强化如下prompt` inside the final INTENT body.",
    "Do not manually grep session jsonl files when read-session-context can return the needed chat payload.",
    "Do not output methodology sections, rollback narration, or temporary field names.",
    "Keep the final publication in the single INTENT shape.",
    "Do not re-expand the result back into a multi-section execution contract unless a downstream consumer explicitly requests it."
  ]
}
```
</part_B>
