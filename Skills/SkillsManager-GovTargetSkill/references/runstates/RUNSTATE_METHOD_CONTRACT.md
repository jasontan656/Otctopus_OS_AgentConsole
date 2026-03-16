# Runstate Method Contract

- target skill: `SkillsManager-GovTargetSkill`
- governed_type: `skill_flow_orchestrator`
- applicability: `applicable`

## Required Checklists
- `Skills_runtime_checklist`
- `workflow_runtime_checklist`
- `stage_runtime_checklist`

## Behavior Contract
- 下一步必须消费上一步产物。
- 每个原子步骤结束后立即回填 checklist。
- 回填结果继续驱动下一步，而不是允许模型跳步或并步。

## Success Criteria
- Skill-flow, workflow, and stage runstate templates all exist.
- Host skill markdown references Skills_runtime_checklist, workflow_runtime_checklist, and stage_runtime_checklist as active governance artifacts.
- Host skill markdown states that downstream skill outputs and prior-stage outputs must be consumed before continuing.
- Host skill markdown states that writeback drives the next step and forbids step skipping or parallel completion.
