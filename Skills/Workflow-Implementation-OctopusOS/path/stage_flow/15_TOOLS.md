---
doc_id: workflow_implementation_octopusos.path.stage_flow.tools
doc_type: topic_atom
topic: Implementation stage tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具之后进入校验条件。
---

# implementation 工具面

## 当前技能 CLI
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage implementation --json`
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py stage-doc-contract --stage implementation --json`
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py stage-command-contract --stage implementation --json`
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py construction-plan-lint --require-execution-eligible --json`
- `python3 ./Skills/Workflow-Implementation-OctopusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
