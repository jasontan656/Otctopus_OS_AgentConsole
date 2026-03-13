---
doc_id: "meta_runtime_selfcheck.turn_end_selfcheck_workflow"
doc_type: "topic_atom"
topic: "Turn-end selfcheck workflow for current-run diagnosis and repair triage"
node_role: "topic_atom"
domain_type: "workflow"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Turn-end selfcheck is the default runtime branch under the skill contract."
  - target: "REPAIR_WRITEBACK_CONTRACT_human.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Turn-end selfcheck decides whether same-turn repair-writeback is needed."
  - target: "FINAL_REPLY_MERGE_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Detected issues must be merged into the same final reply."
---

# DIAGNOSE_WORKFLOW

<part_A>
- 本文件说明默认 `turn end` 自检路径，不再是“只有任务结束后手动复盘”的分支。
- 自检目标是先判断本轮是否顺利；顺利则跳过，不顺利才进入问题分类、自修判断与建议合并。
- 具体运行前仍应先读取 runtime contract。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_turn_end_selfcheck",
  "directive_version": "2.0.0",
  "doc_kind": "workflow",
  "topic": "turn-end-selfcheck",
  "purpose": "Run a default turn-end selfcheck before final reply; skip output when the run is smooth, otherwise diagnose pain points and decide whether immediate same-turn repair is safe.",
  "instruction": [
    "Enter this workflow near turn end, before sending the final reply.",
    "Treat the current turn's tool runs, failures, retries, user corrections, path mistakes, and hesitation as first-class evidence.",
    "Skip emitting selfcheck content when no material problem, confusion, or recoverable waste occurred."
  ],
  "workflow": [
    "Check whether the turn had any tool failure, script failure, path misuse, repeated retry, user correction caused by misunderstanding, or obvious hesitation.",
    "If none are present, mark selfcheck as skipped and continue directly to the normal final reply.",
    "If issues are present, classify them into: immediately repairable in this turn, document/tooling/skill improvements to propose, and unresolved risks that must be disclosed.",
    "When a bounded fix is safe and within the active repo boundary, repair first; otherwise keep the issue as an optimization item.",
    "Merge concise selfcheck findings into the same final reply instead of opening a separate meta-only report."
  ],
  "issue_checklist": [
    "Tool command failed due to wrong path, wrong working directory, wrong entrypoint, or missing governed environment",
    "The model hesitated, looped, retried blindly, or explored too many branches before converging",
    "The user had to correct intent, terminology, path, trigger wording, or missing assumptions",
    "A skill description, routing rule, trigger phrase, or default prompt caused confusion",
    "A script, CLI contract, or runtime contract was misleading, too implicit, or maze-like",
    "The final answer could hide a recoverable execution flaw that should instead feed skill/tool evolution"
  ],
  "optimization_example_list": [
    "Tighten a skill description so trigger semantics are clearer",
    "Adjust keyword or tone wording so the right skill triggers earlier",
    "Fix a wrong default path, runtime root, or repo-local environment instruction",
    "Add a missing example, payload shape, checklist, or boundary rule to a skill document",
    "Simplify a CLI usage contract that caused unnecessary trial-and-error",
    "Patch a local tool or workflow document when the defect is proven and low-risk to repair now"
  ],
  "rules": [
    "Do not emit selfcheck text when the turn was smooth enough that the extra section would be noise.",
    "Do not describe failures without naming the missing guidance, document, script, workflow boundary, or decision gap.",
    "Do not use selfcheck as an excuse for unrelated broad refactors.",
    "If the model can safely repair the issue now, prefer repair plus concise disclosure over merely reporting the problem."
  ]
}
```
</part_B>
