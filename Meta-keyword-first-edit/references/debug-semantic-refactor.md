# Semantic-First Debug Refactor

## Goal
Replace patch-first thinking with semantic correction of the module or feature intent.

## Read-First Checklist (逐字通读)
- Read the smallest complete unit of meaning before editing: the full function, module, workflow step, or spec section.
- Build a minimal “intent + invariants” statement: what must remain true before/after.
- Trace the data and control flow across boundaries (callers, config, IO, state).
- Identify whether the failure is a *meaning mismatch* (wrong contract) or a *missing capability* (new behavior required).

## Workflow
1. Define the intended meaning and invariants of the module.
2. Identify the smallest semantic mismatch that causes the failure.
3. Replace or redesign the core logic or naming that encodes the mismatch.
4. Re-evaluate whether any patch is still needed; add only if replacement cannot express the fix.

## Signals That A Patch Is Wrong
- The fix adds special-case branches without clarifying intent.
- The fix grows conditionals but leaves the core meaning ambiguous.
- The fix depends on fragile ordering or hidden state.
- The fix requires repeating the same guard in multiple places (missing single source of truth).
- The fix “works” only for one dataset/environment because it encodes incidental details.

## Minimal Addition Criteria
- No replacement can encode the requirement without breaking existing intent.
- The new rule is orthogonal and cannot be expressed as a renaming or logic swap.
- Addition introduces a genuinely new capability (new state, new IO, new API surface), not just a rewording.

## Common Replacement Moves (Code)
- Replace scattered guards with a single validator (one choke point).
- Replace ambiguous names with contract names (inputs/outputs/states become explicit).
- Replace implicit order with explicit state machine or dependency ordering.
- Replace duplicated logic with one shared function (then adjust meaning in one place).
