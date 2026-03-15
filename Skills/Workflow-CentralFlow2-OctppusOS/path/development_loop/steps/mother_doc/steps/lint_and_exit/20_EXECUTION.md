---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.lint_and_exit.execution
doc_type: action_execution_doc
topic: Mother doc lint and exit execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 完成当前步骤校验。
---

# lint_and_exit 执行

- 刷新根索引。
- 执行 mother_doc lint。
- 记录是否满足进入 `construction_plan` 的退出门。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
