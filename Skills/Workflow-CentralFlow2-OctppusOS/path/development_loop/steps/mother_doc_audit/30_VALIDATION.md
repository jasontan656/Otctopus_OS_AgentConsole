---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc_audit.validation
doc_type: action_validation_doc
topic: Mother doc audit validation
---

# mother_doc_audit 阶段校验

- `mother-doc-lint` 已通过。
- `mother-doc-audit` 已输出结构化 debt 结果。
- 对 actionable debt，已存在可消费的 shadow split proposal 与 matched registry recipe。
- 若存在 blocking 级 growth debt，当前树尚未允许进入 `mother_doc`。
- 只有当 `audit_gate_allowed=true` 时，才能把当前树当成后续 `mother_doc` 的可靠需求入口继续深读。
