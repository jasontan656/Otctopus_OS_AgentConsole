---
name: refactor-runnable-codes
description: Subskill for behavior/contract-preserving refactors of runnable artifacts (code/tools/runners), especially when there is no requirements doc and code is the only source of truth. Requires extracting a Behavior Contract from entrypoints, defining a matrix-derived witness set, and verifying equivalence with executable oracles (golden master/snapshots/assertions/traces) before and after the change.
---

# Refactor — Runnable Codes

## When To Use
Use this subskill when the artifact is **runnable** and its behavior is primarily determined by **machine execution**, such as:
- Code modules and libraries
- CLIs and tools
- Runners/executors/orchestrators implemented as code
- Scripts that write artifacts to disk or emit machine-readable outputs

If the change also touches natural-language workflows/prompts, use this subskill together with `refactor-prompt-workflows`.

## Goal
Preserve **workflow semantics** and **observable contracts** while changing internals.

Two supported modes (must be specified in the OEC):
- `strict_refactor`: no externally observable changes unless explicitly allowed.
- `contract_preserving_upgrade`: allows UX/presentation/performance improvements while preserving workflow semantics and protected observability contracts.

## Hard Requirements
This subskill is explicitly designed to prevent "patch-driven refactors" that keep chasing isolated regressions.

Hard gates (must all pass before changing code):
- You must define an **OEC**.
- You must produce a **System Model v1** (bounded, structured; see template below).
- You must produce a **Contract Matrix v1** (bounded table; see template below).
- You must define a **witness set derived from the Contract Matrix** (not free-form).
- Each witness case must have an **oracle**: a repeatable equivalence check.
- You must **baseline** the witness set *before* changing the artifact.
- You must not claim equivalence unless you can point to the oracle results.
- Quality gain must not come from deleting observables (e.g., removing diagnostic channels or key outputs), unless explicitly listed in `allowed_deltas`.

Anti-pattern (forbidden):
- Large unstructured enumeration of "potential issues" or "possible edge cases" without a contract matrix, clear stop conditions, and executable oracles.

## No-Doc Refactor Protocol (Code-Only) (Hard)
When there is no requirements/spec doc, treat the **current code behavior** as the only authority.
Do not refactor by intuition. Refactor only after you "decompile" the code into a checkable **Behavior Contract** and lock it down with regressions.

### A. Decompile Code Into a Behavior Contract (Hard)
Goal: convert implementation into **behavior statements** that are reproducible, observable, and assertable.

#### A-1. Entrypoint-Driven Backtrace (Hard)
Start from *all triggers* (entrypoints), then trace the call chain down to externally observable results.

Entrypoints to enumerate (pick what exists, keep bounded):
- CLI commands, flags, env vars, config files, working directory assumptions
- Public APIs (exported functions/classes), plugin hooks
- HTTP routes, RPC handlers, message consumers
- Cron/timers, file watchers, background workers
- UI/TUI event handlers, keymaps, focus changes

For each entrypoint, trace and record the behavior chain:
`Trigger (inputs/context) -> State Change -> Output Change -> Side Effects`

#### A-2. Minimal Behavior Statement (Hard)
Write only *phenomena*, not implementation. Each statement must be:
- Reproducible: given the trigger, it occurs
- Observable: you can see it in state/output/UI
- Assertable: you can check true/false

#### A-3. Behavior Statement Template (Hard)
Prefer a structured block per statement to prevent "hand-wavy equivalence":

```yaml
behavior_statements:
  - id: "B-01"
    strength: "Hard | Soft | Undefined"
    trigger: "<event/call/timing + preconditions>"
    state_change: "<state fields that must change + boundaries/defaults/priority>"
    output_change: "<render/output deltas: schema, DOM, class, text, layout, aria, etc.>"
    side_effects: "<IO/network/cache/log/metrics: must happen or must not happen; counts/order/idempotency>"
```

#### A-4. Constraint Strength (Hard)
Every statement must be labeled to stop refactors from "rationalizing" unintended changes:
- `Hard`: must not change.
- `Soft`: may change but requires explicit explanation and new oracle coverage.
- `Undefined`: behavior is unstable or unobserved; do not promise it, but do note it as a risk.

Mapping rule (Hard):
- Contract Matrix rows must be derived from `behavior_statements` (by id). No free-form "edge case dumping".

## OEC Guidance (Runnable Artifacts)
In addition to the shared OEC fields, runnable artifacts typically require explicit observables like:
- Output artifacts: file set, schema, stable field names
- Exit/status: exit code classes, success/failure categories
- Protocol markers: stable tokens/markers required by downstream consumers
- Idempotency: rerun behavior (merge-only vs overwrite vs append)
- Protected observability: diagnostic/log/event channels that must not disappear or change semantics

## System Model v1 (Hard, bounded)
You must summarize the runnable artifact as a small, checkable model. Keep it short and structural.

Template (fill in; keep it compact):
```yaml
system_model_v1:
  modules:
    - name: "<module/package>"
      responsibility: "<one sentence>"
  state:
    - name: "<state var / persistent state>"
      owner: "<module>"
      lifecycle: "<created/updated/cleared when>"
  event_flow:
    - stimulus: "<CLI arg / keypress / file change / timer tick>"
      path: "<entrypoint -> handlers -> effects>"
  io_contracts:
    reads:
      - "<path/pattern or external dependency>"
    writes:
      - "<path/pattern + merge/overwrite semantics>"
  failure_modes:
    - "<class of failure> -> <observable behavior>"
```

## Contract Matrix v1 (Hard, bounded)
The contract matrix is the finite surface that replaces infinite enumeration.

Rules:
- Max 20 rows in the first pass. If you need more, you must **cluster** and raise abstraction (do not keep adding rows).
- Each row must be testable: it must have a stimulus and an oracle.

Template:
```yaml
contract_matrix_v1:
  - id: CM-01
    contract: "<one externally observable rule>"
    stimulus: "<how it is triggered>"
    observables:
      - "<what must be true>"
    oracle: "<diff/snapshot/assertion/trace invariant>"
    allowed_delta: "<if any>"
    risk_if_broken: "<impact>"
```

## Witness Set Baseline (Hard)
Witness cases MUST be selected from `contract_matrix_v1` (by id). This is how we avoid infinite case enumeration.

Before refactoring, produce baseline evidence per witness case:
- Golden master: normalized output snapshot(s) to diff against after the change
- Snapshot assertions: machine-checkable assertions over key fields/markers/events
- Trace invariants: normalized phase/state/event sequence comparison

If outputs are nondeterministic:
- Define normalization rules first (sorting, stable keys, redaction of timestamps/ids), then baseline.

## Regression-as-Documentation (Hard)
When there is no doc, regression is the doc. The baseline is the ground truth.

### B-1. Golden Master (Fastest Path) (Hard)
Goal: freeze "what it actually does today" into a baseline, then diff after refactor.

You must define, per witness case:
- `input_script`: the exact input sequence to run (events/calls/time/concurrency).
- `observables`: at least one logical output and one presentation output when applicable.
- `diff_policy`: which diffs fail, which diffs are tolerated, and what is whitelisted/blacklisted.

Template:
```yaml
golden_master:
  - witness_id: "CM-01"
    input_script: "<commands/events/calls + ordering>"
    observables:
      - kind: "state_snapshot | output_artifact | structure | attributes | visual | trace"
        capture: "<how to capture>"
    diff_policy:
      mode: "hard | tolerant"
      normalize:
        - "<sort keys, redact timestamps, stable ordering>"
      allowlist:
        - "<fields allowed to change>"
      denylist:
        - "<fields forbidden to change>"
```

Notes (Hard):
- For `tolerant` diffs, normalization comes first. Do not accept raw noise as "ok".
- If you add normalization, it becomes part of the contract. Document it.

### B-2. Property/Invariants Tests (Higher ROI for Core Semantics)
Where possible, add invariant tests that do not overfit exact outputs.

Common invariant categories:
- Boundary invariants: never crash, never go out of bounds, never emit illegal values
- Consistency invariants: derived == base mapping stays consistent
- Idempotency invariants: repeated run does not create extra side effects
- Order invariants: same input sequence produces stable phase/event ordering
- Accessibility invariants: focus/role/aria/tabIndex semantics do not regress (for UI/TUI)
- Performance invariants: upper bounds on render/request/call counts for key operations

### Interactive/UIs (Hard)
If the runnable artifact is interactive (TUI/GUI/event-loop), treat the following as **protected contracts** unless explicitly listed in `allowed_deltas`:
- Input routing (who receives keys/events)
- Focus model (which pane/widget is active)
- Keymap semantics (what a key does in a given focus)
- Selection-to-view coupling (changing selection updates the right view)

In such cases, your witness set must include at least:
- One **trace-based** witness: a recorded sequence of stimuli and a normalized summary of observables to replay and compare.

## Equivalence Verification Checklist
Unless explicitly allowed in `allowed_deltas`, you must preserve:
- Primary outputs (files / payload schemas / required markers)
- Success/failure classification and exit codes (if applicable)
- Ordering/phase semantics (if the consumer relies on it)
- Protected observability contracts:
- Channels still exist
- Semantics unchanged
- Additive-only is allowed, removal is forbidden unless explicitly approved

## Stop Condition (Hard)
You may stop expanding the matrix/cases when:
- Contract Matrix covers all externally visible surfaces relevant to the consumer(s), and
- Every witness case has a runnable oracle, and
- Baseline evidence is captured, and
- A diff policy exists for each golden/snapshot oracle (hard vs tolerant + normalization rules).

## Execution Strategy (No-Doc Safe Refactor) (Hard)
Do not start structural changes until contracts + baselines exist.

Risk ladder (use smallest step that achieves the goal):
- Low risk: renames, extract constants, split functions, file organization, comment improvements (no dataflow changes)
- Medium risk: extract modules/components/services while preserving IO and oracles
- High risk: change state model, event system, rendering strategy, concurrency, caching (requires the strongest regression guardrails)

Per-step rules:
- Each step must be small, revertible, and verified by running the witness set.
- If a step fails an oracle, stop and fix or roll back; do not "continue and hope".

## Output Contract (What To Report)
When done, report in Chinese:
- OEC summary (mode, invariants, allowed deltas)
- System Model v1 (short)
- Contract Matrix v1 (bounded)
- Behavior statements summary (Hard/Soft/Undefined)
- Witness set (matrix-derived cases + oracle)
- Baseline method (golden master / snapshots / traces) and per-witness diff policy
- Equivalence verification result (PASS/FAIL) with oracle evidence
- One measurable quality gain proxy
