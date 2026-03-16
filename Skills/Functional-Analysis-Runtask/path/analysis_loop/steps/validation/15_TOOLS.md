---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.validation.tools
doc_type: action_tool_doc
topic: Validation tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 validation 校验。
---

# validation 阶段工具

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage validation --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage validation --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage all --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
