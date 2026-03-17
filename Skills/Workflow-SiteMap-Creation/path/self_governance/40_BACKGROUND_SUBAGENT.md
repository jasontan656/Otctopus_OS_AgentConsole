---
doc_id: workflow_sitemap_creation.path.self_governance.background_subagent
doc_type: workflow_entry
topic: Background subagent execution for self governance
reading_chain:
- key: artifact_refresh
  target: 50_ARTIFACT_REFRESH.md
  hop: next
  reason: subagent 完成 skill 改造后，主 AGENT 必须回读结果并刷新实验产物。
---

# Background Subagent

- 主 AGENT 必须在 background terminal 中通过 `tmux` 启动单个 SUBAGENT。
- 该 SUBAGENT 的模型参数固定为：
  - model：`gpt-5.4`
  - reasoning effort：`high`
- 主 AGENT 必须持续轮询 tmux 输出、日志与退出状态，不得 fire-and-forget。
- 只有连续 `10` 分钟没有任何新输出时，主 AGENT 才允许判定该 SUBAGENT 已卡死并手工终止；启动阶段较重，不得提前误杀。
- 该 SUBAGENT 的正式输入只能是：
  - factory payload
  - `$Meta-Enhance-Prompt` 产出的 `INTENT:`
  - `Functional-Analysis-Runtask` task runtime / workspace / stage checklist 落点
- SUBAGENT 必须显式执行 `Functional-Analysis-Runtask analysis_loop` 九阶段：
  - `research`
  - `architect`
  - `preview`
  - `design`
  - `impact`
  - `plan`
  - `implementation`
  - `validation`
  - `final_delivery`
- architect / preview / impact / plan / validation 不得折叠回 research、design 或简单写盘步骤。
- `design` 阶段必须显式使用 `$Meta-keyword-first-edit` 决策：
  - 删掉重写
  - keyword-first 替换
  - 最小必要新增
- `implementation` 与 `validation` 必须产生真实对象化证据写回；`validation` 必须在 backend terminal 中做真实交互验证。
- 任务完成后，由主 AGENT 手工终止 tmux 内该单进程并做结果回读。
