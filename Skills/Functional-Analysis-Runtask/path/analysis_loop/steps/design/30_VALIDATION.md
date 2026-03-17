---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.design.validation
doc_type: action_validation_doc
topic: Design validation
---

# design 阶段校验

- 设计对象必须引用有效的 research/architect/preview 输入；design 阶段不得要求 impact 作为输入。
- `design/decisions.yaml` 必须包含 consumed stage reports、问题框架、decision chain、selected strategy、decision items、rejected options 与 evidence refs。
- 每个 decision item 都必须写清问题、所承接的前序报告、被拒绝路径、selected because、rationale 与 evidence refs。
- `design/001_design_strategy.md` 必须存在，且不得残留占位文本，并必须具备阶段目标、消费的前序产物、关键设计问题框架、候选路径与取舍、设计推导链、selected strategy、写回对象与进入 impact 的门禁。
- 若阶段标记完成，`architect` 与 `preview` 不能仍是 `pending`。
