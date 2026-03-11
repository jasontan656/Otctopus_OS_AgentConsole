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
- Consume the file-type `骨架生成模版` and create governed file skeletons directly under a user-specified external directory.
- Create the matching skill-internal `治理映射模版` directory and files with one-to-one path alignment.

## Terminology
- `骨架生成模版`: the initialization-only template surface used by `scaffold`.
- `治理映射模版`: the long-lived skill-internal mapping that later participates in `collect` and `push`.
- `scaffold` is the bridge between these two surfaces: it uses the former to create the first version of the latter.

## Current AGENTS Rule
- `scaffold` currently supports `AGENTS.md`.
- External `AGENTS.md` scaffold must contain `Part A only`.
- Internal `AGENTS_human.md` scaffold must contain internal `Part A + Part B` as part of the initial `治理映射模版`.
- Internal `AGENTS_machine.json` scaffold must exist, remain valid json, and belong to that same initial `治理映射模版`.

## Output
- `scaffold` writes the external skeleton.
- `scaffold` writes the initial internal `治理映射模版` files.
- `scaffold` updates the scan rule asset so the new external target becomes part of the governed scope.
- `scaffold` syncs the same managed result into the installed skill directory.

## Boundary
- `scaffold` creates skeletons only; it does not finalize governed content.
- After initialization, later truth maintenance must happen on the `治理映射模版` side rather than by reinterpreting the `骨架生成模版` as a long-term source of truth.
- User governance still decides the eventual concrete file content after the skeleton exists.
