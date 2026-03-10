# Skill Runtime Contract

> This skill is currently in a no-tool convergence state.
> The previous CLI surface has been removed.

- contract_name: `meta_default_md_manager_no_tool_runtime_contract`
- contract_version: `2.0.0`
- validation_mode: `archival`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

- skill_name: `Meta-Default-md-manager`
- skill_state: `no_active_tools`
- runtime_guidance: use static governance documents only; do not assume removed scripts still exist

## Current Rule
- Do not invoke legacy `Cli_Toolbox.py` commands.
- Use this directory only as a governance archive until new tooling is rebuilt.
- When maintaining AGENTS governance, review `Part A` and `Part B` together.
- External `AGENTS.md` is `Part A only`.
- Internal `AGENTS_human.md` is `Part A + Part B`.
- Internal `AGENTS_machine.json` is `Part B only`.

## Current References
- `references/runtime_contracts/AGENTS_ASSET_GOVERNANCE.md`
- `references/runtime_contracts/AGENTS_PAYLOAD_ARCHIVE.json`
