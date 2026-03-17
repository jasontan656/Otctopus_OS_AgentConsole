---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.design.contract
doc_type: action_contract_doc
topic: Design contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 design 合同，再看工具。
---

# design 阶段合同

- design 必须强制使用 `Meta-keyword-first-edit`，优先按 `rewrite -> replace -> add` 收敛实现策略。
- design 只消费 research、architect 与 preview 已正式落盘的产物；impact 必须发生在 design 之后，不得在 design 阶段偷写 impact 结论。
- design 必须先问透本阶段专属问题：有哪些候选路径、为什么保留/推翻/升级、selected strategy 为什么能同时承接 architect judgement 与 preview projection。
- `design/decisions.yaml` 必须写透：consumed stage reports、问题框架、decision chain、selected strategy、decision items、rejected options 与 evidence refs。
- 每个 decision item 都必须写清问题、所承接的前序报告、被拒绝路径、selected because、rationale 与 evidence refs，不能只写主观偏好。
- `design/001_design_strategy.md` 必须至少写透：阶段目标、消费的前序产物、关键设计问题框架、候选路径与取舍、设计推导链、selected strategy、写回对象与进入 impact 的门禁。
- design 不得提前写 impact、plan、implementation 或 validation 完成态内容。
- 未明确 selected strategy 或未写清 rejected options 前，design 不得标记完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
