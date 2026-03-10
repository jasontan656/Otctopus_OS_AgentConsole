# Cli_Toolbox Usage

## Commands
- `python3 scripts/Cli_Toolbox.py scaffold`
- `python3 scripts/Cli_Toolbox.py scan`
- `python3 scripts/Cli_Toolbox.py lint`
- `python3 scripts/Cli_Toolbox.py collect`
- `python3 scripts/Cli_Toolbox.py push`
- `python3 scripts/Cli_Toolbox.py target-contract --source-path "<external AGENTS path>"`

## Shared Flags
- `--dry-run`
- `--json`
- `--write-runtime-report`
- `--only <substring>`
- `--source-path <absolute external path>`
- `--report-path <custom json path>`

## Stage Notes
- `scaffold` creates governed directory skeletons and the matching internal managed mapping.
- `scan` reads external rule assets and discovers governed files.
- `lint` validates discovered files against the governed structure contracts.
- `collect` treats external files as the source of truth, creates or refreshes matching managed structure, and syncs mirror plus installed skill assets.
- `push` treats internal managed templates as the source of truth and overwrites external targets.
