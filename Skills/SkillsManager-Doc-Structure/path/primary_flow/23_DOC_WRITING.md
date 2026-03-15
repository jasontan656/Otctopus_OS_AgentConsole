---
doc_id: skillsmanager_doc_structure.path.primary_flow.doc_writing
doc_type: topic_atom
topic: Doc writing responsibilities in the primary governance flow
anchors:
- target: 22_PATH_CHAINING.md
  relation: implements
  direction: upstream
  reason: Doc writing checks follow path chaining.
- target: 24_ANCHOR_LINT.md
  relation: routes_to
  direction: downstream
  reason: Anchor lint follows after doc writing checks.
---

# 文档职责检查

## 当前动作
- 检查 `SKILL.md` 是否只保留门面。
- 检查 `00_*_ENTRY.md` 是否只做入口说明和下一跳列表。
- 检查合同、tool/lint、执行、校验等说明是否分散在自己的节点里，而不是重新写回总则。

## 当前动作必须满足什么
- 单个文档只承担当前层的职责。
- 若某段规则只属于某个步骤，就必须下沉到该步骤文档里。
- 不允许把“整个技能所有规则”重新集中回一个总索引。

## 下一跳列表
- [anchor lint]：`24_ANCHOR_LINT.md`
