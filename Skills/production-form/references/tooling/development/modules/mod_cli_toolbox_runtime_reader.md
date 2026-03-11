# Module: cli_toolbox_runtime_reader

## Responsibilities
- Read the working contract for the current temporary product-form phase.
- Read the current product intent snapshot.
- Read the latest local product-form history.
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
