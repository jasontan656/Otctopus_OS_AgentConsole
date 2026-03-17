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

- final_delivery 只能消费 validation 已完成的验收报告与全部前序阶段产物。
- final_delivery 必须先问透本阶段专属问题：对人类真正需要交付的最终结论、关键承接链、剩余风险与后续观察点是什么。
- `final_delivery/001_final_delivery_brief.md` 必须至少写透：交付目标、消费的前序产物、对人类的最终结论、关键承接链摘要、剩余风险与后续观察点。
- final_delivery 不得重新引入新实现、新设计、新影响面分析或新验收判断。
- final_delivery 中任何一句话都必须能回指 validation 或更早阶段的正式产物；若不能回指，视为越权新增结论。

## 下一跳列表
- [tools]：`15_TOOLS.md`
