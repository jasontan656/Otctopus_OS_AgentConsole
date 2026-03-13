---
doc_id: meta_enhance_prompt.runtime.output_governance_contract
doc_type: topic_atom
topic: Output governance mirror for Meta-Enhance-Prompt
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This human mirror records the output governance contract routed from the facade.
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
    "The file written by --output-path must contain the publication body only, never the JSON machine payload.",
    "CLI stdout remains available for direct consumption, but JSON mode stdout and text publication artifacts must stay semantically separate."
  ],
  "workflow": [
    "Resolve the workspace-aware runtime root and result root.",
    "Append machine and human run logs under the runtime root.",
    "Write the emitted publication body to the explicit path or the default result path for the active mode.",
    "If JSON mode is enabled, emit the machine payload to stdout only and keep the file artifact as plain publication text."
  ],
  "rules": [
    "Do not hardcode author-machine absolute workspace paths.",
    "Do not silently write result files under the skill source tree or the installed codex skill tree.",
    "Preserve stdout delivery while making governed file artifacts discoverable.",
    "Do not mirror the same JSON payload into both stdout and the publication output file."
  ],
  "migration_note": "Legacy behavior previously emitted stdout/stderr only, and later JSON mode also wrote JSON payloads into output artifacts. The governed implementation now keeps machine payloads on stdout while materializing only plain publication text and runtime logs under the resolved governed roots."
}
```
</part_B>
