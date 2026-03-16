---
doc_id: workflow_constructionplan_octopusos.path.stage_flow.tools
doc_type: topic_atom
topic: Construction plan stage tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具之后进入校验条件。
---

# construction_plan 工具面

## 当前技能 CLI
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py stage-checklist --stage construction_plan --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py stage-doc-contract --stage construction_plan --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py stage-command-contract --stage construction_plan --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py construction-plan-init --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py construction-plan-lint --json`
- `python3 ./Skills/Workflow-ConstructionPlan-OctopusOS/scripts/Cli_Toolbox.py mother-doc-state-sync --json`

## 共享工作目录
- `construction_plan_root`: `Octopus_OS/Development_Docs/mother_doc/execution_atom_plan_validation_packs`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
