---
doc_id: "meta_runtime_selfcheck.final_reply_merge_contract"
doc_type: "topic_atom"
topic: "Final reply merge contract for selfcheck findings"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Final reply merge is one runtime branch under the main contract."
  - target: "DIAGNOSE_WORKFLOW_human.md"
    relation: "implements"
    direction: "upstream"
    reason: "Turn-end selfcheck findings feed into final reply merge."
  - target: "REPAIR_WRITEBACK_CONTRACT_human.md"
    relation: "supports"
    direction: "cross"
    reason: "Self-repair outcomes must also be merged into the final reply."
---

# FINAL_REPLY_MERGE_CONTRACT

<part_A>
- 本文件约束如何把自检结果和同回合自修结果合并进同一个 final reply。
- 用户原始任务答案始终是主叙事；自检只在有实质问题时追加，不制造噪音。
- 本文件不负责 pain provider 的内部呈现，只负责用户可读输出边界。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_final_reply_merge_contract",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "final-reply-merge",
  "purpose": "Govern how selfcheck findings, same-turn repairs, and optimization items are merged into the same final reply without overwhelming the main user answer.",
  "instruction": [
    "Keep the user's main task answer first; selfcheck findings are appended only when issues materially affected the run.",
    "Merge only high-signal items: what went wrong, what was fixed now, what still needs improvement, and what should change next time.",
    "When selfcheck was skipped, emit nothing about selfcheck in the final reply."
  ],
  "workflow": [
    "Answer the user's original request normally.",
    "If turn-end selfcheck found material issues, append a concise selfcheck section in the same final reply.",
    "State whether each item was self-repaired now, only diagnosed, or left as a suggested improvement.",
    "Prefer a short issue list or short paragraph over a long audit dump."
  ],
  "rules": [
    "Do not let selfcheck overshadow the user's requested answer.",
    "Do not dump raw pain-provider internals into the final reply.",
    "Do not repeat low-value noise when the run was effectively smooth."
  ]
}
```
</part_B>
