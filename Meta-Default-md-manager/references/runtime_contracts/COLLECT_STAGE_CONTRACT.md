# Collect Stage Contract

- contract_name: `meta_default_md_manager_collect_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `archival`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

## Scope
- This document defines only the `collect` stage.
- It does not define scan behavior.
- It does not define push behavior.
- It does not redefine AGENTS asset governance beyond the collect boundary.

## Purpose
- Recover governed external content back into the skill-managed human template.

## AGENTS Rule
- `collect` reads external managed `AGENTS.md`.
- `collect` extracts only external `Part A`.
- `collect` updates only internal `AGENTS_human.md` `Part A`.
- `collect` must not overwrite internal `Part B`.

## Boundary
- `collect` does not push content outward.
- `collect` does not rebuild machine payloads by itself.
- `collect` must stop if the target file shape does not satisfy the governed structure contract.
