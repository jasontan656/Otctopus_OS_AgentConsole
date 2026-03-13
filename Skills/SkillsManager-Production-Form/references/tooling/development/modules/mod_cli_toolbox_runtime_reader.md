---
doc_id: skillsmanager_production_form.references_tooling_development_modules_mod_cli_toolbox_runtime_reader
doc_type: topic_atom
topic: 'Module: cli_toolbox_runtime_reader'
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Module: cli_toolbox_runtime_reader

## Responsibilities
- Read the working contract for the current console-productization phase.
- Read the current console intent snapshot.
- Read the latest local console-productization history.
- Append new local design-log entries in a structured markdown format.

## Inputs
- `working-contract`
- `intent-snapshot`
- `latest-log`
- `append-iteration-log`

## Guarantees
- Machine-readable contract stays in JSON.
- Intent snapshot stays in markdown.
- Log appends are additive.
- The active log sink stays under `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`.
- The repo-side `references/runtime/ITERATION_LOG.md` remains a migration seed snapshot only.
- CLI command routing stays on the Python `typer` baseline.
