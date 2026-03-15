---
doc_id: skillsmanager_doc_structure.path.primary_flow.anchor_scope_rules
doc_type: topic_atom
topic: Anchor scope rules in doc-structure governance
anchors:
- target: 24_ANCHOR_LINT.md
  relation: implements
  direction: upstream
  reason: This file refines anchor-scope review.
- target: 24B_ANCHOR_ALLOWED_RELATIONS.md
  relation: routes_to
  direction: downstream
  reason: Allowed anchor relations follow scope review.
---

# Anchor 作用域规则

## 语义审查规则
- anchor 只能补充当前物理结构已经存在的必要关系。
- anchor 不能替代目录结构承担主导航职责。
- anchor 不能把读者拉回已废弃的旧主组织轴。

## 不合格信号
- 用 anchor 代替缺失的中间节点。
- 用 anchor 直接越过当前层跳向深层正文。
- 把所有关系都写成 anchor，导致物理结构失去意义。

## 下一跳列表
- [anchor 允许关系规则]：`24B_ANCHOR_ALLOWED_RELATIONS.md`
