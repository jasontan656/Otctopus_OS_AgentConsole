---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.research.validation
doc_type: action_validation_doc
topic: Research validation
---

# research 阶段校验

- manifest 必须包含分析 id、目标范围、来源资产、执行模式与阶段状态。
- evidence registry 至少要记录可追溯证据入口与位置。
- `task_runtime.yaml` 必须已经生成完整九阶段骨架，且默认 checklist 为空数组。
- `research/001_research_report.md` 必须存在，并能被 architect 阶段直接消费。
- research report 不得残留占位文本，且必须同时具备：调研目标与范围、输入资产与当前前提、问题框架与强制追问、证据登记、显式推导链、阶段结论、未收口问题与进入 architect 的门禁。
- research 若已完成，不能只剩 evidence registry 而缺少问题链、追问链、显式假设与未收口问题。
- 本地路径引用必须存在，或显式写明是外部 URL。
