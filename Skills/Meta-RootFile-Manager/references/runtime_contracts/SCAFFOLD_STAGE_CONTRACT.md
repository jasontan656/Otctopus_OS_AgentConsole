---
doc_id: meta_rootfile_manager.references_runtime_contracts_scaffold_stage_contract
doc_type: topic_atom
topic: Scaffold Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

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
- When the external target is under `Codex_Skill_Runtime/<skill>/...`, scaffold must place the internal managed asset under that runtime root as well, instead of writing repo-tracked `assets/managed_targets/...`.
- Runtime-local scaffold targets must remain ephemeral: they must not be registered back into `rules/scan_rules.json`, must not sync into the installed skill copy, and must be rediscovered from runtime-local managed assets on later scans.

## Boundary
- `scaffold` is only initialization.
- Long-term truth source still flips between `collect` and `push`.
