---
doc_id: skillsmanager_doc_structure.path.primary_flow.validation_node_rules
doc_type: topic_atom
topic: Validation-node semantic rules in doc-structure governance
reading_chain:
- key: reading_chain_lint
  target: 24_READING_CHAIN_LINT.md
  hop: next
  reason: Reading-chain lint follows the node-role semantic review.
---

# 校验节点规则

## 语义审查规则
- 校验节点只写如何判断当前动作是否完成。
- 可以写通过条件、检查方式和失败回看位置。
- 不应在这里新增新的实施规则。

## 不合格信号
- 校验页重新开始写执行步骤。
- 校验页承担下一个动作的正文。
- 校验页混入全局总则。

## 下一跳列表
- [reading-chain 检查]：`24_READING_CHAIN_LINT.md`
