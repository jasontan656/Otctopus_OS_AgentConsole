---
doc_id: meta_rootfile_manager.references_tooling_cli_toolbox_usage
doc_type: topic_atom
topic: Cli_Toolbox Usage
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Cli_Toolbox Usage

## Commands
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py contract --json`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py scaffold`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py scan`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py lint`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py collect`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py push`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<external AGENTS path>"`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`

## Shared Flags
- `--dry-run`
- `--json`
- `--write-runtime-report`
- `--only <substring>`
- `--source-path <absolute external path>`
- `--report-path <custom json path>`

## Stage Notes
- `contract` returns the skill-level CLI runtime entry set.
- `scaffold` consumes the `骨架生成模版`, creates governed directory skeletons, and writes the first matching `治理映射模版`.
- `scan` reads external rule assets and discovers governed files.
- `scan` skips runtime-managed `ephemeral_workspace/...` targets unless they are explicitly requested through `--source-path`.
- `lint` validates discovered files against the governed structure contracts.
- `collect` treats external files as the source of truth, creates or refreshes the `治理映射模版`, and syncs mirror plus installed skill assets.
- `push` treats the `治理映射模版` as the source of truth and overwrites external targets.
- `target-contract`, `scan`, `collect`, `push`, and `scaffold` all surface a path-derived `owner`.
- `agents-payload-contract` is the mandatory entry for governed `AGENTS_machine.json` payload edits; it returns the target-specific `$Meta-Enhance-Prompt -> payload writeback -> collect -> lint` workflow.
- If the managed content is json, `owner` is embedded into that json.
- If the managed content is not json, `owner` is embedded through frontmatter in the same managed file.
