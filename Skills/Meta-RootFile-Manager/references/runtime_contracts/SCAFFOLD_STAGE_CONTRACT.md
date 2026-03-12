# Scaffold Stage Contract

- contract_name: `meta_rootfile_manager_scaffold_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- `scaffold` initializes a concrete governed root file target at a user path.

## Runtime Rule
- `scaffold` must resolve the file kind to an existing channel.
- `scaffold` must create both:
  - the external file
  - the channel-specific internal managed asset
- For `AGENTS.md`, scaffold creates the human/machine pair.
- For non-`AGENTS.md`, scaffold creates the internal mapped copy with the same initial content as the external file.

## Boundary
- `scaffold` is only initialization.
- Long-term truth source still flips between `collect` and `push`.
