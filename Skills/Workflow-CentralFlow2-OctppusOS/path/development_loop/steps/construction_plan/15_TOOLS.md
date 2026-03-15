---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.construction_plan.tools
doc_type: action_tool_doc
topic: Construction plan tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 工具面之后进入执行说明。
---

# construction_plan 阶段工具面

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage construction_plan --json`
- `python3 ./scripts/Cli_Toolbox.py stage-doc-contract --stage construction_plan --json`
- `python3 ./scripts/Cli_Toolbox.py stage-command-contract --stage construction_plan --json`
- `python3 ./scripts/Cli_Toolbox.py stage-graph-contract --stage construction_plan --json`
- `python3 ./scripts/Cli_Toolbox.py construction-plan-init --json`
- `python3 ./scripts/Cli_Toolbox.py construction-plan-lint --json`

## 模板与支撑面
- `templates/execution_atom_plan_validation_packs/`
- `supporting/`

## 下一跳列表
- [execution]：`20_EXECUTION.md`
