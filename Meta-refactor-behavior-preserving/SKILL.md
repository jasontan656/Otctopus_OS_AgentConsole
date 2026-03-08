---
name: "Meta-refactor-behavior-preserving"
description: Universal migration/refactor protocol across any artifact (prompts, rules/constitutions, workflows, docs/articles, code). Defines “behavior” as observable effects for the relevant consumer, enforces observable-effect equivalence (no new meaning, no lost meaning, triggers still apply), and requires at least one explicit quality gain (load intelligence, decision determinism, run quality).
---

# Meta Refactor — Family Index

## Purpose
Provide a single entrypoint for refactor/migration work that routes to the correct subskill and keeps the family consistent over time.

This family treats “refactor/migration” as a **behavior contract** problem, not an implementation problem.

## Subskill References (authoritative)
```yaml
subskill_reference_map:
  refactor-runnable-codes: references/subskills/refactor-runnable-codes.md
  refactor-prompt-workflows: references/subskills/refactor-prompt-workflows.md
```

## Routing Rules (Hard)
- Runnable artifacts (code/tools/runners/scripts) → use `refactor-runnable-codes`.
- Prompt/workflow/rule artifacts (natural language that drives model actions) → use `refactor-prompt-workflows`.
- Mixed changes → use **both**:
  - Default order: define prompt/workflow contracts first (`refactor-prompt-workflows`), then baseline and enforce executable oracles (`refactor-runnable-codes`).

## Skill Layout Note (Hard, no absolute paths)
- This is a *family skill*. The family root is a router/index and may not contain `scripts/`.
- Always read and follow the detailed protocol from `references/subskills/*.md`.
- If you need to run any helper scripts (now or in the future), resolve them under:
  - `subskills/<subskill>/scripts/<script>.py`
- Resolve `$CODEX_HOME` as:
  - If `$CODEX_HOME` is set: use it.
  - Else: default to `~/.codex`.
- Do NOT guess `scripts/` under the family root.

## Shared Core Concepts (Hard)
Core idea:
- **Behavior = Observable effects**, defined relative to a consumer.
- “Before/after一致” = **Observable-Effect Equivalence**, not textual sameness.
- Migration must also produce at least one **measurable quality gain** (otherwise it is churn).

### Modes (Hard)
You must pick exactly one mode and encode it in the OEC (`mode`):
- `strict_refactor`: no externally observable changes unless explicitly listed in `allowed_deltas`.
- `contract_preserving_upgrade`: user-facing presentation/performance improvements are allowed **only** if listed in `allowed_deltas`, while workflow semantics and protected observability contracts must not regress.

### Observable-Effect Contract (OEC) (Hard)
If you cannot state the OEC, you are not ready to refactor.

```yaml
oec:
  mode: "strict_refactor | contract_preserving_upgrade"
  artifact: "<what is being migrated>"
  consumer: ["<reader|workflow|downstream_model|audit>"]
  stimuli:
    - "<how it is used>"
  observables:
    - "<what must be externally true>"
  invariants:
    - "<must not change>"
  allowed_deltas:
    - "<may change>"
  witness_set:
    - id: "W1"
      stimulus: "<representative stimulus #1>"
      oracle: "<how equivalence is checked (diff/snapshot/assertions)>"
  protected_observability_contracts:
    - "<diagnostic/log/event/output channels that must not disappear or change semantics>"
  quality_gain_targets:
    - "<one explicit improvement target>"
```

### Baseline + Oracle (Hard)
- You must baseline each witness case **before** changing the artifact.
- Each witness case must have a concrete **oracle** (diff/snapshot/assertions), not narrative justification only.
- Quality gains must not come from dropping observables unless explicitly listed in `allowed_deltas`.

## Notes
- This skill is intentionally a router. The detailed protocols live in the referenced subskills.
- Future subskills may be added (e.g., long-form narrative refactors) without expanding this index into a monolith.

## Language Rules
- Chat output must be **Chinese**.
- When drafting documents, default to **Chinese** unless the user specifies otherwise.
- Code blocks, code comments, and code files must be **English only**; do not introduce Chinese inside code.
