---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc_audit.execution
doc_type: action_execution_doc
topic: Mother doc audit execution
reading_chain:
- key: validation
  target: 30_VALIDATION.md
  hop: next
  reason: 完成当前阶段校验。
---

# mother_doc_audit 阶段执行

- 先确认当前 `mother_doc` 根存在并读取 `00_index.md`。
- 先执行 `mother-doc-lint`，确保树协议与根索引干净。
- 再执行 `mother-doc-audit`，识别 overloaded node、未展开语义簇、family drift 与 anchor gap。
- 优先使用 `mother-doc-audit` 输出的 shadow split proposal 与 split decision registry recipe，而不是临时手搓拆分树。
- 对 blocking 级 debt，先完成拆分/迁移与必要注册，再刷新根索引并重跑 lint/audit。

## 下一跳列表
- [validation]：`30_VALIDATION.md`
