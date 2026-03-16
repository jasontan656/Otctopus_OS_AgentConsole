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
- Unified AGENTS maintenance entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-maintain --intent "<natural language request>" --json`
- Narrow AGENTS payload-only entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`
- Scaffold AGENTS finalization entry:
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py new-writeback --json --source-path "<external AGENTS path>"`
- CLI JSON is the primary runtime source.
- Artifact policy:
  `runtime_local_artifacts` via runtime-contract path resolution; repo-tracked mirrors stay under `assets/managed_targets/AI_Projects/...`, while runtime-local mirrors, latest reports, and stage logs stay under `Codex_Skill_Runtime/<skill>/...`.
- Every governed target must expose a path-derived descriptive `owner`.
- If the managed content is json, `owner` must be embedded into that json.
- If the managed content is not json, `owner` must be embedded through frontmatter in the same managed file.
- Normal AGENTS maintenance must enter through `agents-maintain`, which ranks the governed targets, decides `Part A` or embedded payload placement, writes the internal `AGENTS_human.md` truth source, centered-pushes external `Part A`, and then lints.
- Embedded `Part B` payload changes may still use `agents-payload-contract` only when the task is already narrowed to payload-only surgery for a known target.
- `lint` must同时拦截 repo-tracked 孤儿 AGENTS 映射、installed managed targets drift 与 runtime legacy `AGENTS_machine.json` sidecar，避免旧形态静默回流。
- `new-writeback` is the stage that finalizes scaffolded `AGENTS.md + AGENTS_human.md`; the target must not still contain `replace_me`.
- `SKILL.md` remains a facade and narrative mirror.
- Runtime-local or ephemeral sources must store managed mirrors under `Codex_Skill_Runtime/<skill>/managed_targets/...`, not under repo-tracked `assets/managed_targets/...`.
- Default discovery for `scan` / `lint` / `collect` / `push` must exclude runtime-managed targets under `ephemeral_workspace/...` unless the caller explicitly passes that `--source-path`.
- `collect` must not be treated as part of the normal AGENTS maintenance loop; for `AGENTS.md` it remains only for reverse-sync or recovery.
- Latest stage result json must write to `Codex_Skill_Runtime/<skill>/artifacts/<stage>/latest.json`.
- Timestamped run logs must write to `Codex_Skill_Runtime/<skill>/logs/<stage>/`.
