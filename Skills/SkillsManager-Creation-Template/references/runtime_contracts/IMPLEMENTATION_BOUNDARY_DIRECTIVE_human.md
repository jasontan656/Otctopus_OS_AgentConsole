---
doc_id: skillsmanager_creation_template.references.runtime_contracts.implementation_boundary_directive
doc_type: topic_atom
topic: SkillsManager-Creation-Template implementation boundary directive
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This directive documents what belongs in the scaffold and what must stay out.
---

# Implementation Boundary Directive

- Keep stable profile semantics in the scaffold contract.
- Push repo-local conventions, business logic, and runtime result policies down to the generated skill.
- Whenever scripts are generated, generate matching tooling docs and tests in the same run.
