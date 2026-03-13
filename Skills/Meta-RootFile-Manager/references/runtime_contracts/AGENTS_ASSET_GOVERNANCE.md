---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_asset_governance
doc_type: topic_atom
topic: AGENTS Asset Governance Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# AGENTS Asset Governance Contract

## Status
- This document is the current non-executable contract for AGENTS governance inside `Meta-RootFile-Manager`.
- The active CLI implementation must obey this contract.

## Canonical Surfaces

### 0. Template Semantic Boundary
- In this skill, `治理映射模版` means the long-lived skill-internal mapping for a concrete governed target.
- In this skill, `骨架生成模版` means the initialization-only template surface used by `scaffold`.
- `AGENTS_human.md` plus `AGENTS_machine.json` belong to the `治理映射模版` side.
- The scaffold defaults that create first-time AGENTS files belong to the `骨架生成模版` side.
- Structure contracts such as `AGENTS_content_structure.md` are not either template type; they only constrain shape.

### 1. External `AGENTS.md`
- External managed `AGENTS.md` files must contain `Part A only`.
- External files are the human-readable runtime entry layer.
- External files must not carry the machine payload from `Part B`.

### 2. Internal `AGENTS_human.md`
- Internal managed `AGENTS_human.md` is the canonical human audit surface inside the `治理映射模版`.
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
- It is the machine-readable payload source for CLI output.
- It must not duplicate `Part A`.
- It belongs to the same `治理映射模版` instance as the paired `AGENTS_human.md`.

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
- the structured runtime payload that CLI output should return
- JSON objects and arrays that define execution modes, runtime constraints, must-use rules, forbidden patterns, turn contracts, and contract handoff behavior
- `default_meta_skill_order` as the only place that may carry `skill name + minimal description` entries inside the payload
- repo-local payload fields that are meant for deterministic machine consumption

### Part B Forbids
- free-form human entry prose that belongs in `Part A`
- duplicated copies of the direct human entry instructions unless they are intentionally normalized into payload fields
- content that should only exist as a shell command or a plain-language entry note
- repeating any skill name from `default_meta_skill_order` inside other action-oriented payload fields just to restate the same routing or obligation

## Adjacent Contract References
- `scan` semantics are defined in `references/runtime_contracts/SCAN_STAGE_CONTRACT.md`.
- `collect` semantics are defined in `references/runtime_contracts/COLLECT_STAGE_CONTRACT.md`.
- `push` semantics are defined in `references/runtime_contracts/PUSH_STAGE_CONTRACT.md`.
- This document does not expand stage behavior. It only defines how `AGENTS.md` itself is governed.

## Maintenance Rule
- Any AGENTS governance change must be reviewed against both `Part A` and `Part B`.
- Do not update only one side unless the user explicitly scopes the change and the other side is proven unaffected.
- If payload shape or field structure changes, update `AGENTS_human.md`, `AGENTS_machine.json`, and CLI behavior together.
- Do not confuse changes to the long-lived `治理映射模版` with changes to the `骨架生成模版`; the former changes concrete governed content, while the latter changes only initialization defaults.

## Scope Note
- External root `AGENTS.md` and its corresponding internal root managed assets were excluded from the earlier cleanup round.
- That exclusion does not change this contract: the canonical governance model remains `external = Part A only`, `internal human = Part A + Part B`, `internal machine = Part B only`.
