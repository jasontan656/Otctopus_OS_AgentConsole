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
- design 只消费 architect、preview 与 impact 已正式落盘的产物，不得把结构评估、未来形态投影或影响面调研偷渡回来临时补写。
- 必须把实现思路、抽象重整、增删改策略与必要时从零重构判断写成 `design/001_design_strategy.md` 与 `design/decisions.yaml`。
- 每个设计决策都必须引用前序证据或阶段产物，不能只写主观偏好。

## 下一跳列表
- [tools]：`15_TOOLS.md`
