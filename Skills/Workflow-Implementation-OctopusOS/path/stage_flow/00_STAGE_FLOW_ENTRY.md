---
doc_id: workflow_implementation_octopusos.path.stage_flow.entry
doc_type: path_doc
topic: Implementation stage flow entry
reading_chain:
- key: contract
  target: 10_CONTRACT.md
  hop: next
  reason: 先读 implementation 阶段合同。
---

# implementation 阶段入口

## 这个入口是干什么的
- 只服务 `Octopus_OS` 的 `implementation` 阶段。
- 负责消费当前 active pack，并同步回填实现、测试与 pack 证据。

## 下一跳列表
- [contract]：`10_CONTRACT.md`
