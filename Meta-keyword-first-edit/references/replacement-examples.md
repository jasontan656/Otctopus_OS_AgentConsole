# Replacement Examples (Add-less, Replace-first)

This file lists common scenarios where an AI tends to “add more stuff”, but a minimal semantic replacement is usually superior. Use these as teaching patterns, not hard rules.

## Prompts / Workflow Specs

### Phase confusion (plan vs execute)
- Symptom: The model treats planning steps as immediate execution requirements.
- Typical wrong “addition”: Add a long paragraph clarifying phases.
- Preferred replacement:
  - execution -> authoring / planning / writeback
  - 落盘 -> 写回（当目标是写 L10 节点文件，而非实现代码落盘）
  - real path -> read input path (for checklists) / planned target path (for plans)

### Scope leak (a constraint applies only to one field)
- Symptom: “must exist now” intended for a checklist leaks into all mentioned paths.
- Typical wrong “addition”: Add a big “NOTE: only applies to X” section.
- Preferred replacement:
  - must exist now -> must exist now for reading_checklist
  - file path -> reading input file path (for reading_checklist)

### Tone mismatch (logic is fine, but emotional/narrative intent is off)
- Symptom: The document feels too soft/too aggressive compared to intent.
- Typical wrong “addition”: Add a new justification section.
- Preferred replacement (modality/tone):
  - may/should -> must (when it is a hard gate)
  - must -> should (when it is guidance, not a gate)
  - current -> target / after-writeback (when describing future state)

## Documents / Policies

### Duplicate explanation inflation
- Symptom: AI repeats the same rule in multiple new paragraphs.
- Typical wrong “addition”: Add “Summary / Reminder” blocks everywhere.
- Preferred replacement:
  - tighten one sentence so it carries the constraint unambiguously
  - replace vague nouns with scoped nouns (input vs output vs planned)

## Code / Debugging

### Patch stacking for symptoms
- Symptom: Many tiny `if` checks accumulate; behavior becomes fragile.
- Typical wrong “addition”: Add another guard, another flag, another special case.
- Preferred replacement moves:
  - Rename to encode meaning (variable/function names become contracts)
  - Extract “single validator” function and replace multiple scattered checks
  - Replace boolean “mode” with a small enum/state (explicit state machine)

### Adding retries/timeouts as a band-aid
- Symptom: Flakiness, deadlocks, timing issues.
- Typical wrong “addition”: Add retries/sleeps everywhere.
- Preferred replacement:
  - replace blocking call with async/non-blocking design
  - replace implicit ordering with explicit dependencies/state transitions

### Adding a new config knob to hide a design mismatch
- Symptom: “Let’s add a flag so both behaviors exist.”
- Typical wrong “addition”: new config without a stable contract.
- Preferred replacement:
  - replace the contract itself (choose one clear behavior)
  - if two modes are real requirements, encode them via a well-defined state/strategy (then additions are justified)

## Deciding: Replacement vs Addition

Use addition only when the capability truly does not exist:
- New IO surface (new file, new API endpoint, new persistent state)
- New invariant that cannot be expressed by renaming/scoping/modality changes
- New user-facing workflow step that does not exist anywhere

