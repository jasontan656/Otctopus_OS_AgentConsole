# AGENTS Content Structure Contract

## Purpose
- This file defines the governed content structure for `AGENTS.md`.
- It is a structure template only. It does not carry target-specific content.
- Scan lint must use this file to validate whether a discovered `AGENTS.md` matches the required shape.

## External `AGENTS.md` Structure

### Required Blocks
1. `[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]`
2. `` `HOOK_LOAD`: ... ``
3. `<part_A> ... </part_A>`

### Required Shape Rules
- External `AGENTS.md` must contain `Part A only`.
- External `AGENTS.md` must use the explicit `<part_A> ... </part_A>` wrapper in the target shape.
- During transition, collect/lint may temporarily accept legacy `[PART A]` markers from older external files, but push must emit the explicit `<part_A>` shape.
- External `AGENTS.md` must not contain `<part_B> ... </part_B>`.
- `Part A` must be human-readable and directly useful without reading raw json.
- `Part A` may contain:
  - entry commands
  - language rules
  - managed boundary notes
  - multi-agent handling notes
  - other concise direct-read governance instructions

### Forbidden Shape Rules
- External `AGENTS.md` must not embed runtime payload json.
- External `AGENTS.md` must not duplicate the machine-only `Part B`.
- External `AGENTS.md` must not carry internal audit-only sections.

## Internal `AGENTS_human.md` Structure

### Required Blocks
1. `[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]`
2. `` `HOOK_LOAD`: ... ``
3. `<part_A> ... </part_A>`
4. `<part_B> ... </part_B>`
5. a fenced `json` block inside `Part B`

### Required Shape Rules
- Internal `AGENTS_human.md` must contain both `Part A` and `Part B`.
- `Part A` mirrors the external entry content.
- `Part B` mirrors the machine payload in readable markdown form.

## Internal `AGENTS_machine.json` Structure
- `AGENTS_machine.json` must contain `Part B only`.
- It must not duplicate `Part A`.
- It must remain valid json.

## Lint Rule
- If scan discovers `AGENTS.md`, lint must validate it against this contract.
- If scan discovers a newly governed filename without a matching structure template, scan must fail immediately.
