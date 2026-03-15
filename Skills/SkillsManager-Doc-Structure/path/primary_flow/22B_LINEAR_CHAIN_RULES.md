---
doc_id: skillsmanager_doc_structure.path.primary_flow.linear_chain_rules
doc_type: topic_atom
topic: Linear chain rules in doc-structure governance
reading_chain:
- key: doc_writing
  target: 23_DOC_WRITING.md
  hop: next
  reason: Node-writing checks follow after linear chain review.
---

# 单线路径链路规则

## 语义审查规则
- 单线入口内部只能沿闭环顺序向下，不允许再次进入兄弟分支。
- 当前节点之后看到的文件必须仍属于该入口自己的链路。
- 若存在多个入口，它们只能在入口层并列，不能在入口内部再并列。

## 不合格信号
- 在单线入口目录里再出现步骤目录。
- 一个入口文件同时把读者送向两个后续 sibling action loop。
- 用“工具页”同时承担两个入口的共用正文。

## 下一跳列表
- [文档职责检查]：`23_DOC_WRITING.md`
