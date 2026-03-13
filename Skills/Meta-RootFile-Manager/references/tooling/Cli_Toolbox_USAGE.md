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
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py scaffold`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py scan`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py lint`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py collect`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py push`
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<external AGENTS path>"`

## Shared Flags
- `--dry-run`
- `--json`
- `--write-runtime-report`
- `--only <substring>`
- `--source-path <absolute external path>`
- `--report-path <custom json path>`

## Stage Notes
- `scaffold` consumes the `骨架生成模版`, creates governed directory skeletons, and writes the first matching `治理映射模版`.
- `scan` reads external rule assets and discovers governed files.
- `lint` validates discovered files against the governed structure contracts.
- `collect` treats external files as the source of truth, creates or refreshes the `治理映射模版`, and syncs mirror plus installed skill assets.
- `push` treats the `治理映射模版` as the source of truth and overwrites external targets.
- `target-contract`, `scan`, `collect`, `push`, and `scaffold` all surface a path-derived `owner`.
- Every governed target now has a paired owner meta payload; markdown managed copies may also embed `owner` directly for human reading.
