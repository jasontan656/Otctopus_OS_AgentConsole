# Push Stage Contract

- contract_name: `meta_default_md_manager_push_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `archival`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

## Scope
- This document defines only the `push` stage.
- It does not define scan behavior.
- It does not define collect behavior.
- It does not redefine AGENTS asset governance beyond the push boundary.

## Purpose
- Export governed internal content from the `治理映射模版` back to the external target.

## AGENTS Rule
- Internal `治理映射模版` files are the truth source for `push`.
- `push` reads internal `AGENTS_human.md`.
- `push` extracts only internal `Part A`.
- `push` writes only that `Part A` block back to the external `AGENTS.md`.
- `push` must not export internal `Part B`.
- `push` must overwrite the governed external target directly instead of merging by heuristic.

## Boundary
- `push` does not collect external content inward.
- `push` does not export machine json.
- `push` does not use the `骨架生成模版` as an export source.
- `push` must stop if the internal `治理映射模版` human surface shape does not satisfy the governed structure contract.
