# New-File Stage Contract

- contract_name: `meta_rootfile_manager_new_file_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- Defines how a new governed root file type is added into this skill.

## Required Outcome
- Every new file type must open exactly one dedicated `channel`.
- That channel may govern multiple external paths.
- The channel must declare:
  - external `file_kind`
  - `mapping_mode`
  - managed asset filenames
  - governed source path list
  - structure template reference

## Naming Rule
- Non-`AGENTS.md` internal mapped copies must not reuse the external filename directly.
- The managed filename must clearly indicate it is an internal governed mapping of an external root file.

## Boundary
- `new-file` changes the supported governance surface of the skill.
- `new-file` does not instantiate user directories; concrete target creation remains `scaffold`.
