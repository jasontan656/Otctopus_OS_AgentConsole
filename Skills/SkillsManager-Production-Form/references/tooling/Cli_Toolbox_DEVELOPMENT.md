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
- The active local design log must live under `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form`.
- `references/runtime/ITERATION_LOG.md` is now a legacy seed snapshot for first-run migration and bootstrap only.
- The governed result root is `/home/jasontan656/AI_Projects/Codex_Skills_Result/SkillsManager-Production-Form`; future file artifacts must default there unless the caller passes an explicit target path.

## Sync Requirements
- When the CLI changes, update:
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - affected module docs
  - tests
