# Cli_Toolbox Development

## Entry
- Script: `scripts/Cli_Toolbox.py`

## Current Commands
- `working-contract`
- `intent-snapshot`
- `latest-log`
- `append-iteration-log`

## Design Rules
- Keep CLI output deterministic and compact.
- Use `typer` as the CLI framework baseline for Python tooling commands.
- `working-contract` must keep reading the machine-readable JSON contract instead of reconstructing it in code.
- `append-iteration-log` must only append structured markdown entries and must not rewrite earlier history.
- The local design log is console-productization infrastructure; keep it easy to migrate later.

## Sync Requirements
- When the CLI changes, update:
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - affected module docs
  - tests
