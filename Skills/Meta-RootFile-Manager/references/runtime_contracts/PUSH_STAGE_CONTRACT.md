---
doc_id: meta_rootfile_manager.references_runtime_contracts_push_stage_contract
doc_type: topic_atom
topic: Push Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Push Stage Contract

- contract_name: `meta_rootfile_manager_push_stage_contract`
- contract_version: `2.0.0`
- validation_mode: `active`

## Scope
- `push` writes the current managed assets back to the external governed root files.

## Runtime Rule
- For `AGENTS.md`, `push` must export only internal `Part A` back to the external file.
- For every non-`AGENTS.md` channel, `push` must write the internal mapped copy content directly to the external file.
- `push` must preserve the registered external path for the channel target; it must not redirect to a different file path.
- Runtime-local targets under `Codex_Skill_Runtime/<skill>/...` are allowed; `push` must resolve them from runtime-local managed assets rather than repo-tracked managed assets, and no dynamic target registration may be written back into `rules/scan_rules.json`.
- Runtime-managed targets under `Codex_Skill_Runtime/<skill>/managed_targets/ephemeral_workspace/...` are temporary by default and must not be pushed unless the caller explicitly targets them with `--source-path`.
- Missing external targets must not be resurrected by default discovery; they are only eligible for `push` when the caller explicitly supplies the concrete `--source-path`.

## Boundary
- `push` treats the internal managed asset as the truth source for that turn.
