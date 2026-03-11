# Architecture Overview

## Goal
- Give AI a stable local continuity layer for the current Octopus OS product-shaping task.

## Layers
- Facade layer:
  - `SKILL.md`
- Runtime state layer:
  - `references/runtime/WORKING_CONTRACT.json`
  - `references/runtime/CURRENT_PRODUCT_INTENT.md`
  - `references/runtime/ITERATION_LOG.md`
- Tool layer:
  - `scripts/Cli_Toolbox.py`
- Validation layer:
  - `tests/test_cli_toolbox.py`

## Core Flow
1. Read the working contract.
2. Read the current product intent.
3. Read the latest local design-log entry.
4. Make the next product-shaping decision.
5. Append the new decision to the local iteration log.
