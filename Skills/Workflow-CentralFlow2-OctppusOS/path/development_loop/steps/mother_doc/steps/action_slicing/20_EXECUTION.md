---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.action_slicing.execution
doc_type: action_execution_doc
topic: Mother doc action slicing execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 检查本轮切面是否足够小且足够完整。
---

# action_slicing 执行

1. 列出本轮 `must_write` 文档。
2. 列出本轮 `must_read_but_not_write` 文档。
3. 列出本轮 `structure_actions`：
- `vertical_extend`
- `horizontal_branch`
- `edit_existing`
- `delete_or_merge`
- `register_skill_growth_rule`
4. 若动作过多，优先拆成更小切面，而不是一次改完整棵树。
5. 在开始真实编辑前，必须已经知道：
- 写哪
- 为什么写这里
- 为什么不写别处

## 下一跳列表
- [validation]：`30_VALIDATION.md`
