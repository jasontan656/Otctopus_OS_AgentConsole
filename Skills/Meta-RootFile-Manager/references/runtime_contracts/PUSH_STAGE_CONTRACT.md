# Push Stage Contract

- contract_name: `meta_rootfile_manager_push_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- `push` writes the current managed assets back to the external governed root files.

## Runtime Rule
- For `AGENTS.md`, `push` must export only internal `Part A` back to the external file.
- For every non-`AGENTS.md` channel, `push` must write the internal mapped copy content directly to the external file.
- `push` must preserve the registered external path for the channel target; it must not redirect to a different file path.

## Boundary
- `push` treats the internal managed asset as the truth source for that turn.
