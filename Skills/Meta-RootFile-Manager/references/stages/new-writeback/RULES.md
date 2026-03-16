---
doc_id: meta_rootfile_manager.references_stages_new_writeback_rules
doc_type: topic_atom
topic: New Writeback Rules
anchors:
- target: ./ENTRY.md
  relation: elaborates
  direction: upstream
  reason: Rule details for the executable new-writeback stage.
---

# New Writeback Rules

- `new-writeback` only applies to `AGENTS.md`.
- External `AGENTS.md` must not contain `replace_me`.
- Managed `AGENTS_human.md` split domain blocks must not contain `replace_me`.
- `N/A` is allowed when a field is intentionally not applicable to the target.
- If a target has source-specific `Part A` rules, `new-writeback` must respect them before closing.
- `.codex/skills/AGENTS.md` requires `1. 根入口命令` to contain only the single `agents-maintain` CLI entry for that exact target.
- `new-writeback` must run lint before the turn closes.
