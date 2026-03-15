---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.implementation.execution
doc_type: action_execution_doc
topic: Implementation execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 完成当前阶段校验。
---

# implementation 阶段执行

- 实现当前 active pack。
- 执行本 phase 的验证。
- 把 `phase_status.jsonl`、`evidence_registry.json` 与 pack markdown 回填完整。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
