# New-File Stage Contract

- contract_name: `meta_default_md_manager_new_file_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `active`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

## Scope
- This document defines only the `new-file` stage.
- It does not define `scaffold`, `scan`, `collect`, or `push`.

## Purpose
- Add a new governed filename or file type into this skill's supported governance set.

## Workflow Role
- Create the matching structure template for the new governed file.
- Update scan rules, lint requirements, and any tool behavior required to support that file type.
- Validate that dry-run behavior matches the user's governance expectation before real overwrite flows are accepted.
- Sync mirror and installed skill assets, then complete repo traceability for the supporting changes.

## Boundary
- `new-file` changes the skill's supported governance surface.
- `new-file` is not the stage that creates governed directory instances for a user path; that is `scaffold`.
