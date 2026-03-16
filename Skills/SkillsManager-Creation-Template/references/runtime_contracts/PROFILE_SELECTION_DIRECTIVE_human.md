---
doc_id: skillsmanager_creation_template.references.runtime_contracts.profile_selection_directive
doc_type: topic_atom
topic: SkillsManager-Creation-Template profile selection directive
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This directive is part of the governed runtime entry.
---

# Profile Selection Directive

- Pick the smallest stable profile that still matches the target skill.
- Decide `doc_topology` first, then `tooling_surface`, and only then `workflow_control`.
- Generate the final form directly; do not scaffold an old family shape and patch it afterwards.
