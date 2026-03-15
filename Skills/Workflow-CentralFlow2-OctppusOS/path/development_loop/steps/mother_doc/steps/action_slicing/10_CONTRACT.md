---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.action_slicing.contract
doc_type: action_contract_doc
topic: Mother doc action slicing contract
reading_chain:
- key: execution
  target: 20_EXECUTION.md
  hop: next
  reason: 进入当前步骤执行说明。
---

# action_slicing 合同

- 决定动作前，必须先回答：
  - 本轮到底改哪几个原子文档？
  - 哪些文档只需要核对，不需要落盘？
  - 本轮是否需要新增节点、迁移节点或删除节点？
  - 本轮是否需要同步回写 skill 注册表？
- 任何一轮 mother_doc 写回，都应优先收成最小闭环切面；不要把多个独立语义主题绑在同一轮落盘。
- 若用户只是单阶段执行，则本步骤后的“向用户报告”就是当前轮收口；若用户在跑完整闭环，则继续进入后续阶段。

## 下一跳列表
- [execution]：`20_EXECUTION.md`
