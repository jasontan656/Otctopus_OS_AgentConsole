---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.architecture_convergence.tools
doc_type: action_tool_doc
topic: Architecture convergence tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 architecture_convergence 校验。
---

# architecture_convergence 阶段工具

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage architecture_convergence --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage architecture_convergence --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
