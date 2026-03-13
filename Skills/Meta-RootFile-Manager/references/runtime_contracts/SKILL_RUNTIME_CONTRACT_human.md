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
- If the managed content is json, `owner` must be embedded into that json.
- If the managed content is not json, `owner` must be embedded through frontmatter in the same managed file.
- `SKILL.md` remains a facade and narrative mirror.
