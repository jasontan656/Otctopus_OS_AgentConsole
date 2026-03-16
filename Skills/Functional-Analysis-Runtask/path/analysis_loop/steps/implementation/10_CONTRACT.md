---
doc_id: functional_analysis_runtask.path.analysis_loop.steps.implementation.contract
doc_type: action_contract_doc
topic: Implementation contract
reading_chain:
- key: tools
  target: 15_TOOLS.md
  hop: next
  reason: 先读 implementation 合同，再看工具。
---

# implementation 阶段合同

- implementation 只允许读取 active milestone package、其借鉴来源与其要求的证据对象。
- 一旦发生真实实现、验证执行、阶段推进或关键判断更新，必须同步回写 `implementation/turn_ledger.yaml`。
- 若当前切片涉及 task runtime、并发 gate 或阶段状态迁移，必须同步更新对应 `task_runtime.yaml`，不能只写 workspace 对象。
- 不得先修改真实实现，再期望在 turn 结束时凭记忆补证据。

## 下一跳列表
- [tools]：`15_TOOLS.md`
