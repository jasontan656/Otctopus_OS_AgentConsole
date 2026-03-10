# Skill Runtime Contract

> This skill currently exposes an active CLI surface.

- contract_name: `meta_default_md_manager_runtime_contract`
- contract_version: `3.0.0`
- validation_mode: `active`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

- skill_name: `Meta-Default-md-manager`
- skill_state: `active_tools`
- runtime_guidance: use static runtime contracts plus the active CLI

## Current Rule
- Active commands:
- `scripts/Cli_Toolbox.py scaffold`
- `scripts/Cli_Toolbox.py scan`
- `scripts/Cli_Toolbox.py lint`
- `scripts/Cli_Toolbox.py collect`
- `scripts/Cli_Toolbox.py push`
- `scripts/Cli_Toolbox.py target-contract`
- shared helper flags include `--dry-run`, `--json`, `--only`, `--source-path`, and `--report-path`
- When maintaining AGENTS governance, review `Part A` and `Part B` together.
- External `AGENTS.md` is `Part A only`.
- Internal `AGENTS_human.md` is `Part A + Part B`.
- Internal `AGENTS_machine.json` is `Part B only`.
- `scaffold` creates governed directory skeletons and matching internal mappings.
- `new-file` is the stage for adding a new governed file type into the skill's support surface.
- `collect` treats external files as truth and syncs mirror plus installed skill assets.
- `push` treats internal managed templates as truth and overwrites external targets.

## Current References
- `references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md`
- `references/runtime_contracts/AGENTS_PAYLOAD_ARCHIVE.json`
