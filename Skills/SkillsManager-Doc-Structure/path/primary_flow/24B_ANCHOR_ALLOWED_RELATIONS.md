---
doc_id: skillsmanager_doc_structure.path.primary_flow.anchor_allowed_relations
doc_type: topic_atom
topic: Allowed anchor relations in doc-structure governance
anchors:
- target: 24A_ANCHOR_SCOPE_RULES.md
  relation: implements
  direction: upstream
  reason: Allowed anchor relations follow scope review.
- target: 30_VALIDATION.md
  relation: routes_to
  direction: downstream
  reason: Final validation closes the governance flow.
---

# Anchor 允许关系规则

## 语义审查规则
- 常见允许关系是：
  - `routes_to`
  - `implements`
- 这些关系必须服务于“逐级读取”而不是打乱逐级读取。
- 若一个关系无法解释为当前层必要关系，就不应保留。

## 不合格信号
- 用 relation 名字掩盖越级跳转。
- anchor 虽然存在，但其关系无法解释当前层为什么需要它。
- 一个文档挂载大量无关 anchors。

## 下一跳列表
- [最终校验]：`30_VALIDATION.md`
