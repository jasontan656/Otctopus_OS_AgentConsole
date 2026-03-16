---
doc_id: workflow_acceptance_octopusos.path.stage_flow.tools
doc_type: topic_atom
topic: Acceptance stage tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具之后进入校验条件。
---

# acceptance 工具面

## 当前技能 CLI
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage acceptance --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py stage-doc-contract --stage acceptance --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py stage-command-contract --stage acceptance --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py acceptance-lint --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py graph-postflight --json`
- `python3 ./Skills/Workflow-Acceptance-OctopusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
