# Runstate Method Contract

- target skill: `Workflow-SiteMap-Creation`
- governed_type: `workflow_runtime`
- applicability: `applicable`

## Required Checklists
- `workflow_runtime_checklist`
- `stage_runtime_checklist`

## Behavior Contract
- 下一步必须消费上一步产物。
- 每个原子步骤结束后立即回填 checklist。
- 回填结果继续驱动下一步，而不是允许模型跳步或并步。
- checklist 必须显式覆盖：
  - factory
  - intent enhance
  - tmux subagent launch / poll / finalize
  - runtask evidence sync
  - artifact refresh
  - validation closeout

## Success Criteria
- Workflow and stage runstate templates exist.
- Target markdown references workflow_runtime_checklist and stage_runtime_checklist as consumed artifacts.
- Target markdown requires each next step to consume previous output and to write back after each atomic step.
- Target runtime must prove tmux polling and nine-stage runtask evidence were written back.
