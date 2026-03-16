---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.research_baseline.tools
doc_type: action_tool_doc
topic: Research baseline tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 research_baseline 校验。
---

# research_baseline 阶段工具

- `python3 ./scripts/Cli_Toolbox.py workspace-scaffold --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage research_baseline --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage research_baseline --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
