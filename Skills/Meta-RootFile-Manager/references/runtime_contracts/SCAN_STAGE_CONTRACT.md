---
doc_id: meta_rootfile_manager.references_runtime_contracts_scan_stage_contract
doc_type: topic_atom
topic: Scan Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Scan Stage Contract

- contract_name: `meta_rootfile_manager_scan_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- `scan` only discovers governed root files already registered by channel.

## Runtime Rule
- `scan` must read `rules/scan_rules.json` for static channel definitions.
- `scan` must discover current governed targets from governed managed assets and runtime-local managed assets instead of a dynamic path list embedded in `rules/scan_rules.json`.
- `scan` must skip runtime-managed targets rooted under `Codex_Skill_Runtime/<skill>/managed_targets/ephemeral_workspace/...` unless the caller explicitly passes the concrete `--source-path`.
- `scan` must return the matched `channel_id` for every discovered file.
- `scan` must report the internal managed asset path set for each match.

## Boundary
- `scan` is not allowed to invent unmanaged files by fuzzy discovery.
- `scan` should discover only paths already declared in the channel registry.
