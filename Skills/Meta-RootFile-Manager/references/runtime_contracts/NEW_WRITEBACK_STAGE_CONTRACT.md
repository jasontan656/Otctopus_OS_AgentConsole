---
doc_id: meta_rootfile_manager.references_runtime_contracts_new_writeback_stage_contract
doc_type: topic_atom
topic: New Writeback Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# New Writeback Stage Contract

- contract_name: `meta_rootfile_manager_new_writeback_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `active`

## Scope
- `new-writeback` finalizes scaffolded `AGENTS.md` targets after the agent decides how to fill the skeleton according to the user request.

## Runtime Rule
- `new-writeback` applies only to `AGENTS.md` governed targets.
- The agent must replace every scaffold placeholder with either a concrete final value or `N/A` before running this stage.
- `new-writeback` must fail if external `AGENTS.md` or managed `AGENTS_human.md` still contains `replace_me` in the visible contract surface or any Part B domain block.
- After validation passes, `new-writeback` must re-render `AGENTS_human.md` from the external shell-free visible contract surface plus the resolved split Part B domain blocks, while preserving internal frontmatter metadata, and then run lint.
- Source-specific external entry rules remain active during `new-writeback`; for `.codex/skills/AGENTS.md`, `1. 根入口命令` must be a single CLI command that resolves the unified `agents-maintain` entry, not prose.

## Boundary
- `new-writeback` is not the stage that decides user intent by itself; the agent still decides the fill content.
- `new-writeback` only finalizes the governed writeback result and checks that the scaffold placeholders are gone.
