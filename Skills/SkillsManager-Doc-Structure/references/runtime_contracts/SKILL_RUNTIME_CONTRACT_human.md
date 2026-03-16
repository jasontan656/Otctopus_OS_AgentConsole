---
doc_id: skillsmanager_doc_structure.references.runtime_contracts.skill_runtime_contract
doc_type: topic_atom
topic: SkillsManager-Doc-Structure runtime contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document mirrors the machine runtime contract.
---

# SkillsManager-Doc-Structure Runtime Contract

- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Doc-Structure/scripts/Cli_Toolbox.py contract --json`
- Stable source: `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
- `lint` is the topology-aware structural validator.
- `compile-context` is optional and depends on the detected profile.
