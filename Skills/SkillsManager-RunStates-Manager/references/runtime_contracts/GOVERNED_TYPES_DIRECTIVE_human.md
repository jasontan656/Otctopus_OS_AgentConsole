---
doc_id: skillsmanager_runstates_manager.references.runtime_contracts.governed_types_directive
doc_type: topic_atom
topic: Governed types directive for SkillsManager-RunStates-Manager
---

# Governed Types Directive

- `not_applicable`
  - 目标技能不是 workflow-bearing skill。
- `workflow_runtime`
  - 目标技能至少需要 `workflow_runtime_checklist` 与 `stage_runtime_checklist`。
- `skill_flow_orchestrator`
  - 目标技能还需要 `Skills_runtime_checklist`，用于治理技能编排 flow。
