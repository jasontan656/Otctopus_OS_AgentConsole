---
doc_id: workflow_implementation_octopusos.path.stage_flow.contract
doc_type: topic_atom
topic: Implementation stage contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 读完合同后看共享工具面。
---

# implementation 阶段合同

## 当前动作要完成什么
- 严格按 active pack 实现代码、测试和证据写回。
- 只消费 pack 声明的 source refs，不重新发明第二套 scope。

## 当前动作必须满足什么
- pack 已被证明 execution-eligible。
- 本地验证先于状态推进。
- 任何设计偏移都必须通过证据或 ADR 显式落盘。

## 下一跳列表
- [tools]：`15_TOOLS.md`
