# Scan Stage Contract

- contract_name: `meta_default_md_manager_scan_stage_contract`
- contract_version: `1.0.0`
- validation_mode: `archival`
- required_fields:
- `contract_name`
- `contract_version`
- `validation_mode`
- optional_fields:
- `notes`

## Scope
- This document defines only the `scan` stage.
- It does not define AGENTS asset governance.
- It does not define collect or push behavior.

## Purpose
- Discover all files that match the governed scan rules.
- Apply the disallowed list and exclude blacklisted domains such as `Octopus_OS`.
- Produce either stdout output or json output.
- Produce the authoritative candidate list that later `collect` and `lint` consume.

## Rule Source
- Future scan tooling must read exact filename rules, keyword rules, and disallowed lists from external runtime assets.
- Manual keyword rules must support shapes such as `keyword: "contract"` and `file_ext: "*.md"`.

## Output
- stdout output is allowed.
- json output is allowed.
- When json output is selected, the result file must be written under the corresponding `Codex_Skill_Runtime` folder.
- Dry-run output is allowed and should be the default safety path before any later overwrite stage is executed.

## Lint Hook
- Scan must run structure lint after discovery.
- If a governed filename has no matching structure template, scan must fail immediately.
- `AGENTS.md` currently maps to `AGENTS_content_structure.md`.
