# Scaffold Stage Contract

- contract_name: `meta_default_md_manager_scaffold_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `active`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

## Scope
- This document defines only the `scaffold` stage.
- It does not define `new-file`, `scan`, `collect`, or `push`.

## Purpose
- Create governed file skeletons directly under a user-specified external directory.
- Create the matching skill-internal managed directory and files with one-to-one path alignment.

## Current AGENTS Rule
- `scaffold` currently supports `AGENTS.md`.
- External `AGENTS.md` scaffold must contain `Part A only`.
- Internal `AGENTS_human.md` scaffold must contain internal `Part A + Part B`.
- Internal `AGENTS_machine.json` scaffold must exist and remain valid json.

## Output
- `scaffold` writes the external skeleton.
- `scaffold` writes the internal managed files.
- `scaffold` updates the scan rule asset so the new external target becomes part of the governed scope.
- `scaffold` syncs the same managed result into the installed skill directory.

## Boundary
- `scaffold` creates skeletons only; it does not finalize governed content.
- User governance still decides the eventual concrete file content after the skeleton exists.
