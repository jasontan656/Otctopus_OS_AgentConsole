# Runstate Success Criteria

- governed_type: `skill_flow_orchestrator`

## Governance Success
- Skill-flow, workflow, and stage runstate templates all exist.
- Host skill markdown references Skills_runtime_checklist, workflow_runtime_checklist, and stage_runtime_checklist as active governance artifacts.
- Host skill markdown states that downstream skill outputs and prior-stage outputs must be consumed before continuing.
- Host skill markdown states that writeback drives the next step and forbids step skipping or parallel completion.
