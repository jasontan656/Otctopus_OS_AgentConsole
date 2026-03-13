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
- `scan` must read `rules/scan_rules.json`.
- `scan` must return the matched `channel_id` for every discovered file.
- `scan` must report the internal managed asset path set for each match.

## Boundary
- `scan` is not allowed to invent unmanaged files by fuzzy discovery.
- `scan` should discover only paths already declared in the channel registry.
