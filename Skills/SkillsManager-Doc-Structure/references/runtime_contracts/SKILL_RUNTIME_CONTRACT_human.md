---
doc_id: skillsmanager_doc_structure.references_runtime_contracts_skill_runtime_contract
doc_type: topic_atom
topic: SkillsManager-Doc-Structure Runtime Contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# SkillsManager-Doc-Structure Runtime Contract

- Full tool entry: `cd Skills/SkillsManager-Doc-Structure && npm run cli -- <command> ...`
- Contract-only compatibility entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source.
- `SKILL.md` remains a facade and narrative mirror.
- 需要 `lint-doc-anchors`、`lint-split-points`、`register-split-decision`、`build-anchor-graph` 或 `rebuild-self-graph` 时，必须从 skill 根目录进入 `npm run cli -- ...`。
- Python wrapper 不提供完整 lint/graph 命令面，只保留 `contract --json` 兼容读取。
