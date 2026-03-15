---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.implementation.contract
doc_type: action_contract_doc
topic: Implementation contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 implementation 合同，再看工具。
---

# implementation 阶段合同

- implementation 只允许读取 active pack 及其声明的 `source_mother_doc_refs`。
- 不得绕过 packs 直接让代码和测试定义真实意图。
- 当前 pack 的 phase ledger 与 evidence 必须同步回填。

## 下一跳列表
- [tools]：`15_TOOLS.md`
