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
