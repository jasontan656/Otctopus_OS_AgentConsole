---
doc_id: skillsmanager_doc_structure.path.primary_flow.branch_index_rules
doc_type: topic_atom
topic: Branch-index semantic rules in doc-structure governance
reading_chain:
- key: reading_chain_lint
  target: 24_READING_CHAIN_LINT.md
  hop: next
  reason: Reading-chain lint follows after branch-index review.
---

# 分支索引节点规则

## 语义审查规则
- 分支索引节点只负责把读者送入若干独立叶子闭环。
- 它本身不承担叶子闭环的合同、执行或校验正文。
- 允许它下面继续出现子目录，但这些子目录必须各自是完整节点。

## 不合格信号
- 分支索引页自己开始写叶子闭环正文。
- 分支索引下面出现没有 `00_*.md` 的散乱目录。
- 分支索引用一个子目录同时承担多个独立闭环。

## 下一跳列表
- [reading-chain 检查]：`24_READING_CHAIN_LINT.md`
