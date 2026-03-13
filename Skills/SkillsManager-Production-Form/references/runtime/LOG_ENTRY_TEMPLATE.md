---
doc_id: skillsmanager_production_form.references_runtime_log_entry_template
doc_type: example_doc
topic: Iteration Log Entry Template
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Iteration Log Entry Template

Use this shape for every new local console-productization entry:

Active sink:
- `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/SkillsManager-Production-Form/ITERATION_LOG.md`

```markdown
## 2026-03-12 12:34:56Z - <title>

- author: `codex`
- summary: <one-sentence summary>
- decisions:
  - <decision 1>
- affected_paths:
  - `<path>`
- risks:
  - <risk>
- next_steps:
  - <next step>
```

Only log console-productization decisions, naming/registry boundary changes, workflow convergence, or meaningful removals of wrong directions.
