---
doc_id: meta_rootfile_manager.references_runtime_contracts_collect_stage_contract
doc_type: topic_atom
topic: Collect Stage Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Collect Stage Contract

- contract_name: `meta_rootfile_manager_collect_stage_contract`
- contract_version: `2.1.0`
- validation_mode: `active`

## Scope
- `collect` pulls external governed root files back into skill-internal managed assets.

## Runtime Rule
- For `AGENTS.md`, `collect` must read the external visible contract surface as shell-free final content and rebuild `AGENTS_human.md` while preserving the existing internal frontmatter metadata and split Part B domain blocks.
- For `AGENTS.md`, `collect` is an exceptional reverse-sync or external recovery path only; it must not be modeled as part of the normal daily maintenance mainline.
- For every non-`AGENTS.md` channel, `collect` must overwrite the internal mapped copy with the exact external file content.
- `collect` must sync changed managed assets into the installed codex copy when the mirror asset changed.
- Before any managed write or installed-skill sync, `collect` must compare the rendered target bytes with the existing file bytes.
- If the bytes are identical, `collect` must skip that write/sync and report the operation as `skipped` instead of refreshing the file.
- When the external governed file lives under `Codex_Skill_Runtime/<skill>/...`, `collect` must keep the managed asset inside the same runtime root and skip installed-skill sync.

## Boundary
- `collect` treats the external file as the truth source for that turn.
- When the task is normal AGENTS maintenance, the truth-source direction is the opposite: update internal `AGENTS_human.md` first and then push outwards instead of routing through `collect`.
- External sources that resolve outside the governed workspace, or inside ephemeral workspace temp containers, must be treated as runtime-local and must store their managed mirrors under `Codex_Skill_Runtime/<skill>/managed_targets/...` instead of repo-tracked `assets/managed_targets/...`.
- Runtime reports must publish `latest.json` under `Codex_Skill_Runtime/<skill>/artifacts/<stage>/` and timestamped run logs under `Codex_Skill_Runtime/<skill>/logs/<stage>/`.
