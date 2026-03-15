---
doc_id: workflow_centralflow2_octppusos.path.development_loop.tools
doc_type: action_tool_doc
topic: Development loop tools
reading_chain:
- key: workflow_index
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: 工具面之后进入主阶段索引。
---

# 开发闭环工具面

## 运行时与编译命令
- `python3 ./scripts/Cli_Toolbox.py runtime-contract --json`
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry development_loop --selection mother_doc,scope_and_runtime --json`
- `python3 ./scripts/Cli_Toolbox.py read-path-context --entry development_loop --selection construction_plan --json`

## 现有兼容命令
- `workflow-contract`
- `target-runtime-contract`
- `stage-checklist`
- `stage-doc-contract`
- `stage-command-contract`
- `stage-graph-contract`
- `graph-preflight`
- `graph-postflight`
- `target-scaffold`
- `template-index`
- `mother-doc-init`
- `mother-doc-archive`
- `mother-doc-lint`
- `mother-doc-refresh-root-index`
- `mother-doc-state-sync`
- `mother-doc-mark-modified`
- `mother-doc-sync-client-copy`
- `construction-plan-init`
- `construction-plan-lint`
- `acceptance-lint`

## 模板与支撑面位置
- `mother_doc` 模板：`steps/mother_doc/templates/`
- `construction_plan` 模板：`steps/construction_plan/templates/`
- `acceptance` 模板：`steps/acceptance/templates/`

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
