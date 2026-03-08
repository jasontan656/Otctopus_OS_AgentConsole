---
name: refactor-prompt-workflows
description: Subskill for behavior/contract-preserving refactors of prompts/workflows/rules where natural language changes the model's decision trajectory (tool calls, routing, writes, and observability). Requires trigger-matrix witness set and trajectory-aware oracles.
---

# Refactor — Prompt Workflows

## Why This Is Different
For prompts/workflows, the artifact is **natural language** that shapes a model's decisions.
Behavior is not just the final outputs; it includes:
- Routing/trigger decisions
- Tool-call trajectories (what tools are called, in what order, with what parameters)
- Write semantics (what gets written, when, and how reruns behave)
- Diagnostic/observability contracts (what signals exist to explain and audit behavior)

Therefore, equivalence cannot be judged by text similarity. It must be judged by **observable effects** under a witness set.

## When To Use
Use this subskill when refactoring:
- Prompts, instruction packs, constitutions, rule sets
- Workflow definitions and routing logic expressed in natural language
- Protocols for tool usage and write-back
- Documents that define how an agent should think, act, and persist artifacts

If the workflow is implemented partly in code, use this subskill together with `refactor-runnable-codes`.

## Goal
Preserve **workflow semantics** and **protected observability contracts** while improving structure, clarity, or runtime characteristics.

Two supported modes (must be specified in the OEC):
- `strict_refactor`: no externally observable changes unless explicitly allowed.
- `contract_preserving_upgrade`: allows UX/presentation/performance improvements while preserving workflow semantics and protected observability contracts.

## Hard Requirements (Hard Gates)
This subskill is explicitly designed to prevent "prompt patching by infinite edge-case enumeration".

Hard gates (must all pass before rewriting the artifact):
- You must define an **OEC**.
- You must produce a **Workflow Model v1** (bounded, structured; see template below).
- You must produce a **Trigger/Contract Matrix v1** (bounded; see template below).
- You must define a **witness set derived from the matrix** (not free-form).
- Each witness case must have an **oracle** (trajectory-aware, not narrative only).
- You must baseline the witness set before edits and re-run it after edits.

Anti-pattern (forbidden):
- Large unstructured lists of "possible cases", "potential regressions", or "things to check" without a bounded matrix and runnable oracles.

## OEC Additions For Prompt/Workflow Artifacts (Hard)
In addition to the shared OEC fields, you must specify:
- `instruction_priority_model`: how conflicts are resolved (hard rules vs preferences).
- `tooling_surface_contract`: allowed tools, call rules, forbidden actions, critical parameter semantics.
- `routing_contract`: trigger conditions and expected routing outcomes.
- `trace_observables`: the minimum stable trace signals (states/phases/events/markers) that must remain.
- `write_semantics`: idempotency, merge rules, rerun behavior, partial-write recovery.
- `protected_observability_contracts`: diagnostic/log/event/output channels that must not disappear or change semantics.

Hard rule:
- Improvements must not come from deleting or silencing protected observability signals, unless explicitly listed in `allowed_deltas`.

## Workflow Model v1 (Hard, bounded)
Summarize the workflow as a small, checkable model (not a prose paraphrase).

Template:
```yaml
workflow_model_v1:
  states:
    - id: "<state_id>"
      purpose: "<one sentence>"
      entry_triggers:
        - "<trigger condition>"
      required_observables:
        - "<marker/log/event/output that must appear>"
  routing_rules:
    - when: "<condition>"
      must_route_to: "<state_id>"
      must_not_route_to: ["<state_id>"]
  tool_surface:
    allowed_tools: ["<tool>"]
    forbidden_actions:
      - "<action>"
  write_semantics:
    - "<artifact>": "<merge/overwrite/idempotency rule>"
```

## Trigger/Contract Matrix v1 (Hard, bounded)
The matrix is the finite surface that replaces infinite enumeration.

Rules:
- Max 20 rows in the first pass. If you need more, you must **cluster** and raise abstraction.
- Each row must have a stimulus and an oracle.

Template:
```yaml
trigger_contract_matrix_v1:
  - id: TM-01
    stimulus: "<input scenario / prompt / state>"
    expected_routing: "<state_id or branch>"
    tool_trajectory_invariants:
      must_call: ["<tool>(<key params>)"]
      must_not_call: ["<tool>"]
    protected_observables:
      - "<trace marker / log / output semantics>"
    oracle: "<trajectory diff / marker presence / output contract assertions>"
    allowed_delta: "<if any>"
```

## Witness Set Construction (Hard)
Witness cases MUST be selected from `trigger_contract_matrix_v1` (by id).

Your witness set must cover the trigger/routing surface, not just "happy path".
Minimum recommended coverage:
- Trigger matrix cases: one per routing branch (including negative cases that must not trigger).
- Write/idempotency cases: first run, rerun, partial-write recovery case.
- Failure/recovery cases: external dependency failure and the expected FastFail vs auto-repair behavior.

Each witness case must include an oracle, such as:
- Trigger outcome: which branch/state must be entered, which must not.
- Tool trajectory invariants: required calls/markers/events must still occur (additive-only allowed).
- Output contract checks: schema/markers/fields present and semantically consistent.

## Handling Nondeterminism (Hard)
Models can vary. To reduce false equivalence claims:
- Prefer stable settings and deterministic normalization rules.
- For critical witness cases, run multiple replays and define a pass threshold.
- Define "forbidden regressions" explicitly (e.g., missing a required state/marker, losing a protected diagnostic channel).

## Stop Condition (Hard)
You may stop expanding the matrix/cases when:
- The matrix covers all routing branches and protected write/observability contracts, and
- Every witness case has a runnable oracle with baseline evidence.

## Equivalence Methods

### A) Narrative artifacts (docs/articles): Semantic Payload Conservation (Hard)
Must satisfy:
- No-add, no-drop, no-distort (claims/constraints/definitions conserved).
Witness oracles (choose at least one):
- Reader question list
- Claim inventory
- Definition inventory

### B) Constraint/rule artifacts (prompts/workflows/constitutions): Constraint-Closure Equivalence (Hard)
Must satisfy:
- Trigger equivalence
- Application equivalence
- Authority coherence (no parallel sources of truth)
- No legacy parallelism (unless explicitly approved)
Witness oracles (choose at least one):
- Trigger matrix
- Output contract check
- Applied constraint set

## Output Contract (What To Report)
When done, report in Chinese:
- OEC summary (mode, invariants, allowed deltas, protected observability contracts)
- Workflow Model v1 (short)
- Trigger/Contract Matrix v1 (bounded)
- Witness set (matrix-derived + oracles)
- Baseline approach (how you captured the "before" evidence)
- Equivalence verification result (PASS/FAIL) with oracle evidence
- One measurable quality gain proxy
