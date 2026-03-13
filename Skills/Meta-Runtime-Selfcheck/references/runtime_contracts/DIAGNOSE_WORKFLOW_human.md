---
doc_id: "meta_runtime_selfcheck.diagnose_workflow"
doc_type: "topic_atom"
topic: "Diagnosis workflow for previous-run pain analysis"
node_role: "topic_atom"
domain_type: "workflow"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Diagnosis flow is one runtime branch under the skill contract."
  - target: "REPAIR_WRITEBACK_CONTRACT_human.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Diagnosis and repair-writeback are sibling flows chosen by user intent."
---

# DIAGNOSE_WORKFLOW

<part_A>
- 本文件说明默认诊断路径，不负责修复回写。
- 只有在运行已经结束、且目标是复盘上一回合时，才进入本 workflow。
- 具体运行前仍应先读取 runtime contract。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_diagnose_workflow",
  "directive_version": "1.0.0",
  "doc_kind": "workflow",
  "topic": "diagnose-workflow",
  "purpose": "Analyze the previous run and emit a pain-context report without entering writeback mode.",
  "instruction": [
    "Use this directive only after the task or run has ended.",
    "Treat the external pain provider as evidence input, not as the user-facing narrative.",
    "Organize the answer around the previous run, not around an abstract framework."
  ],
  "workflow": [
    "Confirm that CODEX_RUNTIME_PAIN_PROVIDER is set or pass --memory-runtime <provider.py>.",
    "Run the default diagnose command with mode token > and session scope forced to all_threads.",
    "Summarize what happened, why it happened, which layer must change, and how the next run avoids the same stall."
  ],
  "rules": [
    "Do not enter 修复 flow unless the user explicitly requested it.",
    "Do not describe tool failures without naming the missing guidance, document, script, or workflow boundary.",
    "Keep the diagnosis focused on proven evidence, remaining unknowns, and concrete remediation targets."
  ]
}
```
</part_B>
