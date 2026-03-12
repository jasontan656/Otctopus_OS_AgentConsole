# Architecture Overview

## Goal
- Give AI a stable local continuity layer for keeping the console directory in a product-shaped state.

## Layers
- Facade layer:
  - `SKILL.md`
- Runtime state layer:
  - `references/runtime/WORKING_CONTRACT.json`
  - `references/runtime/CURRENT_PRODUCT_INTENT.md`
  - `references/runtime/ITERATION_LOG.md` (legacy seed snapshot)
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form/ITERATION_LOG.md` (active runtime log)
- Tool layer:
  - `scripts/Cli_Toolbox.py`
- Validation layer:
  - `tests/test_cli_toolbox.py`

## Core Flow
1. Read the working contract.
2. Read the current console intent.
3. Read the latest local design-log entry from the governed runtime root.
4. Make the next console productization decision.
5. Append the new decision to the local iteration log under the governed runtime root.
