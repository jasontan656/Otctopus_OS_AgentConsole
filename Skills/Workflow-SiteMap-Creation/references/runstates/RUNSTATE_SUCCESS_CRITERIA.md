# Runstate Success Criteria

- governed_type: `workflow_runtime`

## Governance Success
- Workflow and stage runstate templates exist.
- Target markdown references workflow_runtime_checklist and stage_runtime_checklist as consumed artifacts.
- Target markdown requires each next step to consume previous output and to write back after each atomic step.
- Target runtime proves tmux polling, manual termination, nine-stage runtask evidence, artifact refresh, and validation closeout all happened.
