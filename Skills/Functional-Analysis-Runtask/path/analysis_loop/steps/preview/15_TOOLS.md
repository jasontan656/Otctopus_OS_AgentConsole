---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.preview.tools
doc_type: action_tool_doc
topic: Preview tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 preview 校验。
---

# preview 阶段工具

- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage preview --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage preview --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
