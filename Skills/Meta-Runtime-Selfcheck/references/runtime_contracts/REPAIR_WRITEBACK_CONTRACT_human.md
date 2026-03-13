---
doc_id: "meta_runtime_selfcheck.self_repair_writeback_contract"
doc_type: "topic_atom"
topic: "Immediate same-turn self-repair contract after turn-end selfcheck"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Self-repair writeback is a runtime branch under the main contract."
  - target: "OUTPUT_GOVERNANCE_CONTRACT_human.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Self-repair still needs governed runtime logs and result roots."
  - target: "FINAL_REPLY_MERGE_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Self-repair outcomes must be merged into the same final reply."
---

# REPAIR_WRITEBACK_CONTRACT

<part_A>
- 本文件说明同回合即时自修的进入条件与写回边界。
- 自修不再要求用户显式先说“修复”；只要 turn-end 自检已证明该问题局部、可验证、可安全收口，就可进入。
- 若问题超出当前任务边界、过大或无法验证，应停止自修，改为 final reply 内的优化建议。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_self_repair_writeback",
  "directive_version": "2.0.0",
  "doc_kind": "contract",
  "topic": "self-repair-writeback",
  "purpose": "Govern immediate same-turn self-repair when turn-end selfcheck proves that a bounded fix is safe, local, and verifiable.",
  "instruction": [
    "Enter this contract when turn-end selfcheck finds a concrete issue that can be safely repaired in the same turn.",
    "Prefer low-risk, local repairs such as tool usage fixes, skill description fixes, routing fixes, contract wording fixes, or missing example additions.",
    "Whenever a file is changed, collect verification evidence in the same turn and disclose the repair in the final reply."
  ],
  "workflow": [
    "Confirm the fix is within the active repo boundary and does not require speculative broad refactors.",
    "Apply the minimal correct repair first, then run the relevant verification command or inspection step.",
    "If verification succeeds, treat the issue as self-repaired and include the outcome in the final reply.",
    "If repair is unsafe, too broad, or unverifiable, stop repairing and downgrade the item into a final-reply optimization suggestion."
  ],
  "rules": [
    "Do not auto-repair speculative issues without evidence from the current run.",
    "Do not mark a pain item repaired when verification evidence is missing or failing.",
    "Do not let self-repair escape the active task boundary or overwrite unrelated user changes."
  ]
}
```
</part_B>
