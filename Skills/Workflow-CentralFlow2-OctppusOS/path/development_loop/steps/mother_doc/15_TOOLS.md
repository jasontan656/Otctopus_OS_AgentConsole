---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.tools
doc_type: action_tool_doc
topic: Mother doc tools
reading_chain:
- key: workflow_index
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: 工具面之后进入 mother_doc 子 workflow。
---

# mother_doc 阶段工具面

- `python3 ./scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./scripts/Cli_Toolbox.py target-scaffold --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-init --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-refresh-root-index --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-lint --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-mark-modified --auto-from-git --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-sync-client-copy --json`

## 模板与支撑面
- `templates/mother_doc/`
- `templates/agents/`
- `templates/REQUIREMENT_ATOM_TEMPLATE.md`
- `supporting/`

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
