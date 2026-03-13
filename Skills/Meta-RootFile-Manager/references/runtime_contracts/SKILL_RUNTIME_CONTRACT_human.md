---
doc_id: meta_rootfile_manager.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: Meta-RootFile-Manager Runtime Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Meta-RootFile-Manager Runtime Contract

- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<governed external path>" --json`
- CLI JSON is the primary runtime source.
- Every governed target must expose a path-derived descriptive `owner`.
- Markdown managed copies may embed `owner` directly for direct reading.
- Every governed target must persist an owner meta payload even when the external file format cannot safely host an owner field.
- `SKILL.md` remains a facade and narrative mirror.
