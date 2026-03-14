---
doc_id: meta_rootfile_manager.references_stages_new_writeback_entry
doc_type: topic_atom
topic: New Writeback Instruction
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# New Writeback Instruction

> Active stage semantics. This stage finalizes scaffolded `AGENTS.md` targets after the agent fills them according to user intent.

- Fill both external `AGENTS.md` and internal `AGENTS_machine.json`.
- Do not leave `replace_me`; use a concrete value or `N/A`.
- Run `new-writeback` to re-render `AGENTS_human.md` and verify the finalized result.
