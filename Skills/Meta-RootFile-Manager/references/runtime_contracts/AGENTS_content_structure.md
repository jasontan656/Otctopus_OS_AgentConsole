---
doc_id: meta_rootfile_manager.references_runtime_contracts_agents_content_structure
doc_type: topic_atom
topic: AGENTS Content Structure Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# AGENTS Content Structure Contract

## Purpose
- This file defines the governed content structure for `AGENTS.md`.
- It is a structure template only. It does not carry target-specific content.
- It is neither the `治理映射模版` nor the `骨架生成模版`; it only defines the allowed shape that both surfaces must satisfy where applicable.
- Scan lint must use this file to validate whether a discovered `AGENTS.md` matches the required shape.

## External `AGENTS.md` Structure

### Required Blocks
1. `[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]`
2. `` `HOOK_LOAD`: ... ``
3. `<part_A> ... </part_A>`

### Required Shape Rules
- External `AGENTS.md` must contain `Part A only`.
- External `AGENTS.md` must use the explicit `<part_A> ... </part_A>` wrapper in the target shape.
- External `AGENTS.md` must not contain `<part_B> ... </part_B>`.
- External `AGENTS.md` must carry an `owner` field in its readable metadata surface so the file can explain who owns the entry and that it is governed by `$Meta-RootFile-Manager`.
- `Part A` must be human-readable and directly useful without reading raw json.
- `Part A` may contain:
  - entry commands
  - language rules
  - product-facing documentation language boundaries
  - wizard language support notes
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
- Internal `AGENTS_human.md` must also carry the same path-derived `owner` field.

## Internal `AGENTS_machine.json` Structure
- `AGENTS_machine.json` must contain `Part B only`.
- It must not duplicate `Part A`.
- It must remain valid json.
- It must carry an `owner` field.
- It must satisfy the source-path-specific payload structure contract in `AGENTS_payload_structure.json`.

## Lint Rule
- If scan discovers `AGENTS.md`, lint must validate the external entry against this contract.
- `lint` must also validate the paired internal `AGENTS_human.md` and `AGENTS_machine.json` against the current structure lock.
- If scan discovers a newly governed filename without a matching structure template, scan must fail immediately.
