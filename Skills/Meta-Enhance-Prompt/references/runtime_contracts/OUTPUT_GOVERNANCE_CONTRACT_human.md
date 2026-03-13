---
doc_id: "meta_enhance_prompt.runtime.output_governance_contract"
doc_type: "topic_atom"
topic: "Output governance mirror for Meta-Enhance-Prompt"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This human mirror records the output governance contract routed from the facade."
---

# OUTPUT_GOVERNANCE_CONTRACT

<part_A>
- 本分支定义 `Meta-Enhance-Prompt` 的日志与结果文件落点。
- 输出仍可直接从 stdout 消费，但受管文件产物必须进入 runtime/result roots。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_enhance_prompt_output_governance_contract",
  "directive_version": "2.0.0",
  "doc_kind": "contract",
  "topic": "output-governance",
  "purpose": "Govern runtime logs, default result outputs, explicit output paths, and migration notes for Meta-Enhance-Prompt.",
  "instruction": [
    "Runtime logs must default under the governed runtime root derived from the active workspace or codex home fallback.",
    "Final outputs must support an explicit --output-path and otherwise default under the governed result root.",
    "CLI stdout remains available for direct consumption, but file artifacts must still land in the governed roots."
  ],
  "workflow": [
    "Resolve the workspace-aware runtime root and result root.",
    "Append machine and human run logs under the runtime root.",
    "Write the emitted result to the explicit path or the default result path for the active mode."
  ],
  "rules": [
    "Do not hardcode author-machine absolute workspace paths.",
    "Do not silently write result files under the skill source tree or the installed codex skill tree.",
    "Preserve stdout delivery while making governed file artifacts discoverable."
  ],
  "migration_note": "Legacy behavior previously emitted stdout/stderr only. The governed implementation now keeps stdout while also materializing result and runtime log artifacts under the resolved governed roots."
}
```
</part_B>
