---
doc_id: skillsmanager_production_form.path.append_iteration_log.template
doc_type: example_doc
topic: Iteration log entry template
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: Validate the append workflow after reading the template.
---

# Iteration Log Entry Template

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

Only log console-productization decisions, naming or workflow boundary changes, or meaningful removals of wrong directions.
