# Keyword Rewrite Playbook

## Heuristics
- Replace phase-confusing verbs with phase-accurate verbs (plan, writeback, execute, validate).
- Replace overloaded nouns with scoped nouns (input file, planned file, target path).
- Replace absolute terms with bounded terms when scope is narrower (must exist now -> must exist for reading).
- Preserve structure; change only the minimal tokens that flip meaning.
- Prefer intent-aligned modality/tone replacements over new paragraphs (should/must/may; present vs target; hedge vs commitment).
- Prefer renames that encode constraints (read-only input vs planned output; observed state vs desired state).

## When Replacement Is Enough
- The intent is already present but misread.
- The behavior can be corrected by renaming or tightening scope.
- The error stems from ambiguous verbs or missing qualifiers.
- The artifact already contains the rule, but a single word makes it apply too broadly (scope leak).
- The “fix” would otherwise be a new explanatory section that duplicates what a precise word can convey.

## When Addition Is Required
- The intent is not expressed anywhere in the text or logic.
- Replacement would change the meaning of existing, correct requirements.
- A new constraint is mandatory and cannot be encoded by retargeting existing tokens.
- Multiple audiences or modes must be supported and cannot be disambiguated via scoped wording alone.

## Output Template
- old -> new -> reason

## Example Patterns
- execute -> plan
- real path -> read input path
- create first -> plan creation order
- now/current -> target/after-writeback (when describing future state)
- all/any -> reading_checklist only / within scope X (scope bounding)

## Common “Add More Text” Traps (Docs/Prompts)
- Trap: Add a new “clarification paragraph” to explain phases. Prefer verb swap.
  - immediate execution -> immediate writeback planning
  - execute steps -> author steps / plan steps
- Trap: Add a new section to restate scope. Prefer scoping nouns.
  - file path -> read input file path (for checklists)
  - file path -> planned target path (for planned changes)

## Common “Add More Logic” Traps (Code)
- Trap: Add `if special_case: ...` for one symptom. Prefer semantic replacement:
  - rename variables to reflect meaning (e.g., `isReady` -> `hasValidConfig`)
  - replace a boolean flag with a meaningful enum/state (small redesign)
  - move from scattered checks to a single validator function
- Trap: Add “retry/sleep/timeout” everywhere. Prefer replacement at the contract boundary:
  - replace blocking call with non-blocking variant
  - replace implicit ordering with explicit dependency graph/state machine
