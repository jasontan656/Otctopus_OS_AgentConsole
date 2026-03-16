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
- preview 只消费 research 与 architect 已落盘的产物，不直接定义实现策略。
- preview 必须独立落盘 future shape、behavior delta、failure modes 与 rollback triggers，供 design 与 validation 消费。

## 下一跳列表
- [tools]：`15_TOOLS.md`
