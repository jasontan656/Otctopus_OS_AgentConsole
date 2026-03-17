---
doc_id: workflow_sitemap_creation.path.self_governance.entry
doc_type: workflow_entry
topic: Self governance entry for Workflow-SiteMap-Creation
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: 先锁定双重目的输入与写入边界。
- key: runstates
  target: ../../references/runstates/RUNSTATE_METHOD_CONTRACT.md
  hop: side
  reason: workflow runtime 必须消费中间态。
---

# Self Governance Entry

- 当前入口的正式主链固定为：
  - `factory`
  - `intent_enhance`
  - `background_subagent`
  - `artifact_refresh`
  - `validation_closeout`
- factory 不是终点；factory 完成后必须显式调用 `$Meta-Enhance-Prompt`，再把 `INTENT:` 交给 background subagent。
- background subagent 必须以内置的 `Functional-Analysis-Runtask analysis_loop` 九阶段闭环改造 skill 本体。
- 主 AGENT 负责轮询 tmux 输出、等待完成、手工终止单进程、回读结果并刷新实验产物。
- 任何写入前都不得把输入降级成单一产物需求，也不得退化回固定模板重刷。
