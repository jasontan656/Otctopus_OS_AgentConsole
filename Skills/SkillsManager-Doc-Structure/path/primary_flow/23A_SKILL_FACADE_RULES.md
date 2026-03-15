---
doc_id: skillsmanager_doc_structure.path.primary_flow.skill_facade_rules
doc_type: topic_atom
topic: Skill facade semantic rules in doc-structure governance
anchors:
- target: 23_DOC_WRITING.md
  relation: implements
  direction: upstream
  reason: This file starts node-role semantic review.
- target: 23B_ENTRY_NODE_RULES.md
  relation: routes_to
  direction: downstream
  reason: Entry-node rules follow the facade rules.
---

# 门面规则

## 语义审查规则
- `SKILL.md` 只写模型立刻需要知道的事情、功能入口和目录结构图。
- `SKILL.md` 的职责是“把读者送到下一层”，不是承载深层正文。
- 门面不应解释某个具体入口内的详细执行规则。

## 不合格信号
- 把完整 workflow 或步骤正文写回 `SKILL.md`。
- 在门面并列暴露多个深层文档。
- 把原本下沉后的规则重新收回门面。

## 下一跳列表
- [入口节点规则]：`23B_ENTRY_NODE_RULES.md`
