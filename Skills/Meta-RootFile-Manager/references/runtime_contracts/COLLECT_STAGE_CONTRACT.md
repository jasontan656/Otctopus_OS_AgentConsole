---
doc_id: meta_rootfile_manager.references_runtime_contracts_collect_stage_contract
doc_type: topic_atom
topic: Collect Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Collect Stage Contract

- contract_name: `meta_rootfile_manager_collect_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- `collect` pulls external governed root files back into skill-internal managed assets.

## Runtime Rule
- For `AGENTS.md`, `collect` must read external `Part A` and rebuild `AGENTS_human.md`.
- For every non-`AGENTS.md` channel, `collect` must overwrite the internal mapped copy with the exact external file content.
- `collect` must sync changed managed assets into the installed codex copy when the mirror asset changed.

## Boundary
- `collect` treats the external file as the truth source for that turn.
