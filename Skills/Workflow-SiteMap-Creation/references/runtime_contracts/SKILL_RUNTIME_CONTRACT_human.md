# Workflow-SiteMap-Creation Runtime Contract

- runtime rule source: `CLI_JSON`
- skill role: upstream mother_doc architecture producer
- formal mainline:
  - `factory_intake`
  - `intent_enhance`
  - `background_subagent`
  - `artifact_refresh`
  - `validation_closeout`
- `intent_enhance` 固定调用 `$Meta-Enhance-Prompt`
- `background_subagent` 固定以 `tmux` 启动 `gpt-5.4 / reasoning=high`
- `background_subagent` 固定执行 `$Functional-Analysis-Runtask analysis_loop` 九阶段
- `design` 阶段固定显式执行 `$Meta-keyword-first-edit`
