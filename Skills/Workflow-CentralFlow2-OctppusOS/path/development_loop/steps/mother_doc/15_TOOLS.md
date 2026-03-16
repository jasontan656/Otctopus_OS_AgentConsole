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
- `cd <codebase_root> && META_CODE_GRAPH_RUNTIME_ROOT=<graph_runtime_root> node Skills/Meta-code-graph-base/assets/gitnexus_core/dist/cli/index.js status`
- `META_CODE_GRAPH_RUNTIME_ROOT=<graph_runtime_root> node Skills/Meta-code-graph-base/assets/gitnexus_core/dist/cli/index.js analyze <codebase_root>`

## 模板与支撑面
- `templates/mother_doc/`
- `templates/agents/`
- `templates/REQUIREMENT_ATOM_TEMPLATE.md`
- `supporting/`

## 外部技能协作
- `Meta-Impact-Investigation`
  - 用途：在任何 mother_doc 写回前，先判断需求影响面、潜在无锚点关联与回归面。
- `Meta-code-graph-base`
  - 用途：在 repo 已有实质代码时，先确认图谱状态；缺图时先初始化，再用 graph context 校准当前代码现实。

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
