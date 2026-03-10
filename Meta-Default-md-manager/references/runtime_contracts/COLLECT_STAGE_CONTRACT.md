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
- Based on scan results, create or refresh the matching skill-internal directory structure and recover governed external content into the skill-managed template layer.

## AGENTS Rule
- `collect` reads external managed `AGENTS.md`.
- External managed files are the truth source for `collect`.
- `collect` extracts only external `Part A`.
- `collect` creates the corresponding internal managed directory and file shape when missing.
- `collect` updates only internal `AGENTS_human.md` `Part A`.
- `collect` must not overwrite internal `Part B`.
- `collect` must preserve the existing internal `AGENTS_machine.json`.
- `collect` must sync the same managed result into both the Codex skill mirror and the installed skill directory.

## Boundary
- `collect` does not push content outward.
- `collect` does not rebuild machine payloads by itself.
- `collect` must stop if the target file shape does not satisfy the governed structure contract.
