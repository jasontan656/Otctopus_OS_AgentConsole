---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.preview.contract
doc_type: action_contract_doc
topic: Preview contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 preview 合同，再看工具。
---

# preview 阶段合同

- preview 必须强制使用 `Meta-Reasoning-Chain` 的单层链路结构。
- preview 只消费 research 与 architect 已落盘的产物，并且必须在对象层和报告层显式引用这两份正式报告。
- preview 必须先问透本阶段专属问题：如果 architect judgement 成立，未来形态、行为变化、失败模式、回滚阈值分别是什么；哪些只是预测，不能偷渡成设计或实现决定。
- `preview/projection.yaml` 必须写透：consumed stage reports、问题框架、推演链、future shape、behavior delta、failure modes、rollback triggers 与 evidence refs。
- `preview/001_future_shape_preview.md` 必须至少写透：阶段目标、消费的前序产物、关键预演问题框架、future shape、behavior delta、failure modes、rollback triggers、预演推导链与进入 design 的门禁。
- preview 不得直接定义实现策略、文件修改方案或影响面矩阵；这些必须交给后续阶段。
- 若 rollback triggers 写不透，preview 不得标记完成。

## 下一跳列表
- [tools]：`15_TOOLS.md`
