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
- 若要写回 selfcheck 自身，还必须先进入 keyword-first-edit 治理，并在 rewrite/delete 路径上先请求用户确认删除范围。
- 本 workflow 只治理“问题轨”；可优化点要在 turn end 进入独立优化审计轨。
</part_A>

<part_B>

```json
{
  "directive_name": "meta_runtime_selfcheck_turn_hook_self_repair",
  "directive_version": "3.0.0",
  "doc_kind": "workflow",
  "topic": "turn-hook-self-repair",
  "purpose": "Run a default turn hook throughout the active turn; when issue evidence appears, diagnose it immediately and start repair before continuing the main task.",
  "instruction": [
    "Enter this workflow as soon as issue evidence appears anywhere in the active turn, and run a final closure pass before the final reply.",
    "Keep this workflow scoped to the runtime-problem lane; do not swallow optimization points that should be audited after the run completes.",
    "Before executing risky or governed commands, prefer pre-exec-check so the hook can adjudicate normalization or expected-failure handling before the first failure happens.",
    "Use run-turn-hook or watch-codex-sessions as the technical carrier so the hook really runs and leaves turn-audit evidence.",
    "Treat the current turn's tool runs, failures, retries, user corrections, path mistakes, and hesitation as first-class evidence.",
    "When the issue is concrete, local, and verifiable, do not stop at diagnosis; move directly into bounded repair."
  ],
  "workflow": [
    "If a command is about to run and it touches governed Python, lint, repo-local validation, or traceability flows, call pre-exec-check first.",
    "Check whether the current turn has any tool failure, script failure, path misuse, CLI semantic mismatch, repeated retry, user correction caused by misunderstanding, or obvious hesitation.",
    "If none are present, keep the hook quiet and continue the main task.",
    "If CODEX_RUNTIME_PAIN_PROVIDER is absent, fall back to Codex session turn evidence instead of exiting with configuration error.",
    "If issues are present, classify them into: immediately repairable in this turn, not-yet-verifiable but still strengthenable, explicitly allowed expected failures, and residual risks that must be disclosed or escalated.",
    "When the hook strengthens or writes back Meta-Runtime-Selfcheck itself, run keyword-first-edit-governance first so the chosen path is rewrite > replace > add; if rewrite/delete is selected, stop and request user confirmation with explicit deletion scope.",
    "When a bounded fix is safe and within the active repo boundary, repair first, collect verification evidence, and mark the turn audit with resolved optimization ids before continuing.",
    "When a failure matches the expected-failure whitelist, allow it, record it, and carry it into later strengthening or validation artifacts instead of auto-repairing over it.",
    "Leave non-blocking optimization points for the turn-end optimization audit instead of force-routing them into the immediate repair lane.",
    "Do not downgrade directly into advice when a local repair exists; only retain residual risk after the minimal correct repair has been applied."
  ],
  "issue_checklist": [
    "Tool command failed due to wrong path, wrong working directory, wrong entrypoint, or missing governed environment",
    "CLI subcommand/option was invalid but the failure was only discovered after execution, revealing a preflight gap",
    "Installed skill copy or non-canonical runtime surface was used instead of repo truth source",
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
    "Do not auto-kill an expected failing test or lint run when the active stage explicitly whitelisted that failure shape.",
    "If the model can safely repair the issue now, repair first and disclose the outcome later; do not merely report the problem."
  ]
}
```
</part_B>
