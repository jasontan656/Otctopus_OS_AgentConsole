---
doc_id: "meta_runtime_selfcheck.repair_writeback_contract"
doc_type: "topic_atom"
topic: "Explicit repair writeback contract after manual remediation"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Repair writeback is a runtime branch under the main contract."
  - target: "OUTPUT_GOVERNANCE_CONTRACT_human.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Repair writeback still needs governed runtime logs and result roots."
---

# REPAIR_WRITEBACK_CONTRACT

<part_A>
- 本文件只说明显式 `修复` 路径的进入条件与写回边界。
- 修复本身必须先在别处手工落盘，再由本技能负责验证与 resolved writeback。
- 若用户没有明确要求 `修复`，不要进入本分支。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_repair_writeback_contract",
  "directive_version": "1.0.0",
  "doc_kind": "contract",
  "topic": "repair-writeback",
  "purpose": "Govern the explicit 修复 flow after manual changes and verification evidence already exist.",
  "instruction": [
    "Enter this contract only when the user explicitly requested 修复.",
    "Manual changes must already be applied outside this skill before writeback is attempted.",
    "Provide --manual-repair-path and at least one --verify-cmd whenever repair writeback is intended."
  ],
  "workflow": [
    "Run the repair command with 修复 plus --manual-repair-applied.",
    "Allow the skill to verify the changed paths and mark resolved groups only after verification succeeds.",
    "Refresh the pending queue after writeback so the next pain focus is current."
  ],
  "rules": [
    "Do not auto-execute deprecated repair commands.",
    "Do not mark a pain group resolved when verification evidence is missing or failing.",
    "Do not present repair writeback as a substitute for the manual code edit itself."
  ]
}
```
</part_B>
