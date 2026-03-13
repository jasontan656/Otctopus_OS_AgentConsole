---
doc_id: meta_enhance_prompt.runtime.active_invoke_directive
doc_type: topic_atom
topic: Active invoke workflow mirror for Meta-Enhance-Prompt
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This human mirror documents the active invoke workflow routed from the facade.
---

# ACTIVE_INVOKE_DIRECTIVE

<part_A>
- 本分支只负责把已经完成 repo 调研的 `raw_prompt_output` 限形成最终六段合同。
- `active_invoke` 不允许再补默认段落；缺失关键段时必须失败。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_active_invoke_workflow",
  "directive_version": "2.0.0",
  "doc_kind": "workflow",
  "topic": "active-invoke",
  "purpose": "Filter a repo-surveyed raw prompt into the fixed six-section execution contract without inventing missing evidence.",
  "instruction": [
    "Require the raw prompt to already contain GOAL, REPO_CONTEXT_AND_IMPACT, INPUTS, OUTPUTS, BOUNDARIES, and VALIDATION.",
    "Reject missing required sections instead of auto-filling placeholders.",
    "Emit only the filtered final prompt or the machine-readable failure payload.",
    "When the contract body is later published in chat, do not paraphrase or restate GOAL or REPO_CONTEXT_AND_IMPACT outside the contract itself."
  ],
  "workflow": [
    "Read the raw prompt output produced after repo survey.",
    "Run scripts/filter_active_invoke_output.py --mode active_invoke.",
    "Write runtime logs under the governed runtime root and write the pure prompt body to the explicit output path or governed result root.",
    "Publish the filtered final output only if validation succeeds."
  ],
  "rules": [
    "Do not claim repo context was surveyed when the raw prompt does not contain it.",
    "Do not output methodology sections, rollback narration, or temporary field names.",
    "Keep the final prompt in the fixed six-section shape.",
    "Do not add an extra chat-layer summary that repeats GOAL or REPO_CONTEXT_AND_IMPACT before the contract body."
  ]
}
```
</part_B>
