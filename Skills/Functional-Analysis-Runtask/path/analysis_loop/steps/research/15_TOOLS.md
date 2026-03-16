---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.research.tools
doc_type: action_tool_doc
topic: Research tools
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 工具面之后进入 research 校验。
---

# research 阶段工具

- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py contract --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic task-routing --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py directive --topic execution-boundary --json`
- `python3 ../Functional-HumenWorkZone-Manager/scripts/Cli_Toolbox.py paths --json`
- `python3 ./scripts/Cli_Toolbox.py task-gate-check --json`
- `python3 ./scripts/Cli_Toolbox.py task-runtime-scaffold --task-name <slug> --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py workspace-scaffold --workspace-root <path> --json`
- `python3 ./scripts/Cli_Toolbox.py stage-checklist --stage research --json`
- `python3 ./scripts/Cli_Toolbox.py stage-lint --workspace-root <path> --stage research --json`

## 下一跳列表
- [validation]：`30_VALIDATION.md`
