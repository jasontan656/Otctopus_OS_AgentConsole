---
doc_id: skillsmanager_creation_template.references.runtime_contracts.skill_runtime_contract
doc_type: topic_atom
topic: SkillsManager-Creation-Template runtime contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document mirrors the machine runtime contract.
---

# SkillsManager-Creation-Template Runtime Contract

- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/SkillsManager-Creation-Template/scripts/Cli_Toolbox.py contract --json`
- The stable source is the JSON contract under the same directory.
- `profile` returns the supported scaffold catalog.
- `scaffold` writes the final-form skeleton directly for the selected profile.
