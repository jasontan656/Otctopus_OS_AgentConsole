---
doc_id: meta_rootfile_manager.references_stages_new_writeback_flow
doc_type: topic_atom
topic: New Writeback Flow
anchors:
- target: ./ENTRY.md
  relation: elaborates
  direction: upstream
  reason: Flow details for the executable new-writeback stage.
---

# New Writeback Flow

1. Read the scaffolded external `AGENTS.md`.
2. Fill the external `Part A` content according to the user request.
3. Fill the embedded `Part B` payload inside `AGENTS_human.md` according to the user request.
4. Check both surfaces for `replace_me`.
5. Re-render `AGENTS_human.md`.
6. Run lint and stop on any failure.
