---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc_audit.tools
doc_type: action_tool_doc
topic: Mother doc audit tools
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 工具面之后进入 audit 执行。
---

# mother_doc_audit 阶段工具面

- `python3 ./scripts/Cli_Toolbox.py target-runtime-contract --json`
- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage mother_doc_audit --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-lint --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-audit --json`
- 对机器消费方，若需要在保留 fail payload 的同时避免非零退出码打断流程，可改用：`python3 ./scripts/Cli_Toolbox.py mother-doc-audit --json --soft-fail-exit`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-refresh-root-index --json`
- `python3 ./scripts/Cli_Toolbox.py mother-doc-sync-client-copy --json`
- `cd <codebase_root> && META_CODE_GRAPH_RUNTIME_ROOT=<graph_runtime_root> node Skills/Meta-code-graph-base/assets/gitnexus_core/dist/cli/index.js status`

## 目标输出
- protocol lint 结果
- growth debt 审计结果
- matched split decision registry 摘要
- shadow split proposals
- 需要先拆分/迁移的 blocking 节点清单

## 下一跳列表
- [execution]：`20_EXECUTION.md`
