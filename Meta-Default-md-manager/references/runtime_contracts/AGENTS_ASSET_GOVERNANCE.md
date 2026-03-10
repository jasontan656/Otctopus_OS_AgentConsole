# AGENTS Asset Governance Contract

## Status
- This document is the current non-executable contract for AGENTS governance inside `Meta-Default-md-manager`.
- The previous CLI implementation has been removed.
- New tooling must be rebuilt against this contract instead of reviving the removed scripts.

## Canonical Surfaces

### 1. External `AGENTS.md`
- External managed `AGENTS.md` files must contain `Part A only`.
- External files are the human-readable runtime entry layer.
- External files must not carry the machine payload from `Part B`.

### 2. Internal `AGENTS_human.md`
- Internal managed `AGENTS_human.md` is the canonical human audit surface.
- It must contain both explicit blocks:

~~~html
<part_A>
...
</part_A>

<part_B>
```json
{
  "...": "..."
}
```
</part_B>
~~~

- `Part A` mirrors the external-facing entry content.
- `Part B` mirrors the machine payload in readable markdown form.

### 3. Internal `AGENTS_machine.json`
- Internal managed `AGENTS_machine.json` must contain `Part B only`.
- It is the machine-readable payload source for future CLI output.
- It must not duplicate `Part A`.

## Part Boundary Contract

### Part A Allows
- root entry commands or repo-local entry commands that a human must read directly
- stable language rules
- managed boundary notes such as current repo scope
- multi-agent or concurrency handling rules that must remain directly visible
- other concise human-readable entry instructions that belong in the external `AGENTS.md`

### Part A Forbids
- structured machine payload fields
- JSON contract bodies
- execution mode objects
- large routing tables or machine-oriented field schemas
- duplicated copies of `Part B`

### Part B Allows
- the structured runtime payload that future CLI output should return
- JSON objects and arrays that define execution modes, runtime constraints, must-use rules, forbidden patterns, turn contracts, and contract handoff behavior
- repo-local payload fields that are meant for deterministic machine consumption

### Part B Forbids
- free-form human entry prose that belongs in `Part A`
- duplicated copies of the direct human entry instructions unless they are intentionally normalized into payload fields
- content that should only exist as a shell command or a plain-language entry note

## Scan
- `scan` only discovers which files are managed by this skill.
- It keeps the existing filename-driven discovery boundary.
- It does not write managed copies.

## Collect
- `collect` reads external managed `AGENTS.md` files.
- It extracts only the `<part_A> ... </part_A>` block from the governed external shape.
- It updates only the internal human template's `Part A`.
- It must not overwrite the internal `Part B`.

## Push
- `push` reads the internal human template.
- It extracts only the `<part_A> ... </part_A>` block.
- It writes only that block back to the external `AGENTS.md`.
- `Part B` remains internal only.

## Maintenance Rule
- Any AGENTS governance change must be reviewed against both `Part A` and `Part B`.
- Do not update only one side unless the user explicitly scopes the change and the other side is proven unaffected.
- If payload shape or field structure changes, update `AGENTS_human.md`, `AGENTS_machine.json`, and future tool design together.

## Scope Note
- External root `AGENTS.md` and its corresponding internal root managed assets were excluded from the earlier cleanup round.
- That exclusion does not change this contract: the canonical governance model remains `external = Part A only`, `internal human = Part A + Part B`, `internal machine = Part B only`.
