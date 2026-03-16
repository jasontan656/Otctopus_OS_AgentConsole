---
doc_id: meta_rootfile_manager.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: Skill Runtime Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Skill Runtime Contract

- skill_name: `Meta-RootFile-Manager`
- runtime_kind: `channelized_root_file_governance`

## Summary
- This skill governs workspace root files through file-type channels.
- `AGENTS.md` remains a special `A/B` channel.
- Every other supported root file type uses a single internal mapped copy.

## Managed Asset Rule
- External root files remain the files actually consumed by repos.
- Skill-internal assets are mapping versions stored under `assets/managed_targets/AI_Projects/...`.
- Non-`AGENTS.md` managed assets must use explicit governed-mapping filenames instead of the raw external filename.
- Runtime-local or ephemeral sources must not write managed mirrors into repo-tracked skill assets; they must use `Codex_Skill_Runtime/<skill>/managed_targets/...`.

## Runtime Output Rule
- Latest stage result json must live under `Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json`.
- Timestamped stage run logs must live under `Codex_Skill_Runtime/<skill>/logs/<stage>/`.
- Runtime outputs, logs, temp mirrors, and ephemeral managed targets must not default back into the skill directory.
- Default discovery for `scan` / `lint` / `collect` / `push` must skip runtime-managed targets under `ephemeral_workspace/...` unless the caller explicitly targets that source path.
- `push` must also skip missing external targets during default discovery; only explicit `--source-path` can re-target a missing governed file.

## Runtime Source Rule
- `rules/scan_rules.json` is the static channel registry truth source.
- Dynamic governed target discovery must come from governed managed assets under `assets/managed_targets/AI_Projects/...` plus runtime-local managed assets under `Codex_Skill_Runtime/<skill>/managed_targets/...`.
- `target-contract` must return the resolved channel and managed asset paths for the requested external path.
- `contract` must expose the skill-level CLI runtime entry set.
- `agents-maintain` must be the only stable daily maintenance entry for governed `AGENTS.md` work.
- `agents-maintain` must expose governed target ranking, placement-gate results, selected `Part A` or embedded payload location, duplicate/inheritance gate status, mutation mode, and the centered-push write plan in one machine-readable payload.
- `agents-payload-contract` remains available only for explicit payload-only surgery inside `AGENTS_human.md`.
- `lint` must reject child `AGENTS` surfaces that repeat parent `AGENTS.md` or parent payload semantics; skill entries are the only exception.
- `lint` must also reject repo-tracked orphan `AGENTS_human.md` mappings whose external target no longer exists, installed managed-target drift, and runtime legacy `AGENTS_machine.json` sidecars.
- Daily `AGENTS.md` maintenance must update the internal `AGENTS_human.md` truth source first, then push external `Part A`, then lint.
- `collect` must not appear in the normal `AGENTS.md` maintenance mainline; for `AGENTS.md` it is reserved for reverse-sync or external recovery only.
