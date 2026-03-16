---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.design.tools
doc_type: action_tool_doc
topic: Design tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 design 校验。
---

# design 阶段工具

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage design --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage design --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
