---
doc_id: skillsmanager_doc_structure.path.primary_flow.compound_chain_rules
doc_type: topic_atom
topic: Compound chain rules in doc-structure governance
anchors:
- target: 22A_NEXT_HOP_RULES.md
  relation: implements
  direction: upstream
  reason: This file refines the compound chain branch.
- target: 23_DOC_WRITING.md
  relation: routes_to
  direction: downstream
  reason: Node-writing checks follow after compound chain review.
---

# 复合路径链路规则

## 语义审查规则
- 复合技能允许 `workflow index -> step entry -> step-local loop` 逐级下沉。
- `workflow index` 只负责列步骤，不负责承担 step-local 正文。
- 每个 step 进入后，只看到该 step 自己的局部闭环。

## 不合格信号
- `workflow index` 混入各 step 的完整规则。
- step 目录跨读其他 step 的局部文档。
- 用 anchors 直接跳过 `workflow index` 或 `step entry`。

## 下一跳列表
- [文档职责检查]：`23_DOC_WRITING.md`
