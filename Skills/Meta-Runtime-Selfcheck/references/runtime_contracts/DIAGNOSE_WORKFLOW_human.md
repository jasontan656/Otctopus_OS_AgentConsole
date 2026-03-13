---
doc_id: "meta_runtime_selfcheck.turn_hook_self_repair_workflow"
doc_type: "topic_atom"
topic: "Turn hook self-repair workflow for current-run diagnosis and repair triage"
node_role: "topic_atom"
domain_type: "workflow"
anchors:
  - target: "SKILL_RUNTIME_CONTRACT_human.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Turn-hook self-repair is the default runtime branch under the skill contract."
  - target: "REPAIR_WRITEBACK_CONTRACT_human.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Turn hook decides whether same-turn repair-writeback is needed."
  - target: "FINAL_REPLY_MERGE_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Detected issues must be merged into the same final reply."
---

# DIAGNOSE_WORKFLOW

<part_A>
- 本文件说明默认 `turn hook` 路径；一旦当前回合出现问题证据，应立刻进入，而不是等到 `turn end`。
- hook 目标不是只给建议，而是先判断是否存在当前边界内的最小可验证修复，并立即执行。
- 具体运行前仍应先读取 runtime contract。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_turn_hook_self_repair",
  "directive_version": "2.0.0",
  "doc_kind": "workflow",
  "topic": "turn-hook-self-repair",
  "purpose": "Run a default turn hook throughout the active turn; when issue evidence appears, diagnose it immediately and start repair before continuing the main task.",
  "instruction": [
    "Enter this workflow as soon as issue evidence appears anywhere in the active turn, and run a final closure pass before the final reply.",
    "Treat the current turn's tool runs, failures, retries, user corrections, path mistakes, and hesitation as first-class evidence.",
    "When the issue is concrete, local, and verifiable, do not stop at diagnosis; move directly into repair."
  ],
  "workflow": [
    "Check whether the current turn has any tool failure, script failure, path misuse, repeated retry, user correction caused by misunderstanding, or obvious hesitation.",
    "If none are present, keep the hook quiet and continue the main task.",
    "If issues are present, classify them into: immediately repairable in this turn, not-yet-verifiable but still strengthenable, and residual risks that must be disclosed.",
    "When a bounded fix is safe and within the active repo boundary, repair first and collect verification evidence before continuing.",
    "Do not downgrade directly into advice when a local repair exists; only retain residual risk after the minimal correct repair has been applied."
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
    "Do not emit extra hook text when the turn was smooth enough that the extra section would be noise.",
    "Do not describe failures without naming the missing guidance, document, script, workflow boundary, or decision gap.",
    "Do not use selfcheck as an excuse for unrelated broad refactors.",
    "If the model can safely repair the issue now, repair first and disclose the outcome later; do not merely report the problem."
  ]
}
```
</part_B>
