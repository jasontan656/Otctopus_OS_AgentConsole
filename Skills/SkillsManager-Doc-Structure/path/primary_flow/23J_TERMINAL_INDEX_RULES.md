---
doc_id: skillsmanager_doc_structure.path.primary_flow.terminal_index_rules
doc_type: topic_atom
topic: Terminal-index semantic rules in doc-structure governance
anchors:
- target: 23_DOC_WRITING.md
  relation: implements
  direction: upstream
  reason: Terminal-index review is a branch of node-writing review.
- target: 24_ANCHOR_LINT.md
  relation: routes_to
  direction: downstream
  reason: Anchor lint follows after terminal-index review.
---

# 终止索引节点规则

## 语义审查规则
- 终止索引节点可以只保留一个 `00_*.md` 文件。
- 它的作用是登记、索引或暴露最终落点，不再强行继续形成 `10/15/20/30` 闭环。
- 若它通过 anchors 或正文清楚暴露最终落点，就视为合格。

## 不合格信号
- 终止索引节点又长出额外正文层，试图伪装成闭环。
- 终止索引节点下面再挂无意义的空目录。
- 终止索引节点既不是索引，也不承担明确终止作用。

## 下一跳列表
- [anchor lint]：`24_ANCHOR_LINT.md`
