---
doc_id: functional_analysis_runtask.path.analysis_loop.tools
doc_type: action_tool_doc
topic: Analysis loop tools
reading_chain:
- key: workflow_index
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: 工具面之后进入主阶段索引。
---

# analysis_loop 工具面

## 运行时与编译命令
- `python3 ./scripts/Cli_Toolbox.py runtime-contract --json`
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry analysis_loop --selection plan --json`
- `python3 ./scripts/Cli_Toolbox.py read-path-context --entry analysis_loop --selection implementation --json`
- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage plan --json`
- `python3 ./scripts/Cli_Toolbox.py workspace-scaffold --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage all --json`

## 小型对象参考
- `supporting/LIGHTWEIGHT_RUNTASK_OBJECT_MODEL.md`

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
