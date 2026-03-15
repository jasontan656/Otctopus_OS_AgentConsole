---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.steps.impact_and_codegraph.execution
doc_type: action_execution_doc
topic: Mother doc impact and codegraph execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 执行后检查是否满足进入文档树判断的最低证据。
---

# impact_and_codegraph 执行

1. 把当前用户需求收成 `WRITE_INTENT` 影响面。
2. 明确：
- 哪些现有文档必读
- 哪些 sibling/branch 文档虽然无锚点但必须核对
- 哪些代码区域与本轮文档设计直接相关
3. 检查 `graph runtime root`：
- 已存在：读取 `status/context/impact`
- 不存在且 repo 有实质代码：先 `analyze`
- 不存在且 repo 近空：记录缺口后继续
4. 只有在影响面与 graph context 足够支撑判断时，才进入 `protocol_tree` 与后续 growth 决策。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
