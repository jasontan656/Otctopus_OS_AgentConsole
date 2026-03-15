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
- 先确认正文没有重新破坏结构边界。
- 再沿目标技能自己的文档链路做语义审查，判断该层内容是否承担了正确职责。
- 这一步不要求所有技能写成完全相同的正文模板。

## 当前动作必须满足什么
- 单个文档只承担当前层的职责。
- 若某段规则只属于某个步骤，就必须下沉到该步骤文档里。
- 不允许把“整个技能所有规则”重新集中回一个总索引。
- CLI 不检查正文措辞是否一致；模型只检查语义是否越层、错层或重新总则化。

## 下一跳列表
- [anchor lint]：`24_ANCHOR_LINT.md`
