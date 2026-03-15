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

- Primary runtime entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py contract --json`
- Concrete governed target entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<governed external path>" --json`
- Dedicated AGENTS payload entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
- Scaffold AGENTS finalization entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py new-writeback --json --source-path "<external AGENTS path>"`
- CLI JSON is the primary runtime source.
- Every governed target must expose a path-derived descriptive `owner`.
- If the managed content is json, `owner` must be embedded into that json.
- If the managed content is not json, `owner` must be embedded through frontmatter in the same managed file.
- `AGENTS_machine.json` payload changes must go through the dedicated `agents-payload-contract` workflow before writeback.
- `new-writeback` is the stage that finalizes scaffolded `AGENTS.md + AGENTS_machine.json`; the target must not still contain `replace_me`.
- `SKILL.md` remains a facade and narrative mirror.
- Runtime-local or ephemeral sources must store managed mirrors under `Codex_Skill_Runtime/<skill>/managed_targets/...`, not under repo-tracked `assets/managed_targets/...`.
- Latest stage result json must write to `Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json`.
- Timestamped run logs must write to `Codex_Skill_Runtime/<skill>/logs/<stage>/`.
