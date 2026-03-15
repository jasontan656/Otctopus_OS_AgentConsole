---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.acceptance.tools
doc_type: action_tool_doc
topic: Acceptance tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 工具面之后进入执行说明。
---

# acceptance 阶段工具面

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage acceptance --json`
- `python3 ./scripts/Cli_Toolbox.py stage-doc-contract --stage acceptance --json`
- `python3 ./scripts/Cli_Toolbox.py stage-command-contract --stage acceptance --json`
- `python3 ./scripts/Cli_Toolbox.py stage-graph-contract --stage acceptance --json`
- `python3 ./scripts/Cli_Toolbox.py acceptance-lint --json`
- `python3 ./scripts/Cli_Toolbox.py graph-postflight --json`

## 模板与支撑面
- `templates/ACCEPTANCE_REPORT_TEMPLATE.md`
- `templates/ACCEPTANCE_MATRIX_TEMPLATE.md`

## 下一跳列表
- [execution]：`20_EXECUTION.md`
