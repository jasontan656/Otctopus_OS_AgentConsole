---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.final_delivery.contract
doc_type: action_contract_doc
topic: Final delivery contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 final_delivery 合同，再看工具。
---

# final_delivery 阶段合同

- final_delivery 只能消费 validation 已完成的验收报告与前序阶段产物。
- final_delivery 不得重新引入新实现、新设计或新影响面分析。
- final_delivery 必须把最终对人类可见的摘要写入 `final_delivery/001_final_delivery_brief.md`。

## 下一跳列表
- [tools]：`15_TOOLS.md`
