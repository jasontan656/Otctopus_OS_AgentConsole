---
doc_id: skillsmanager_doc_structure.path.primary_flow.entry_node_rules
doc_type: topic_atom
topic: Entry-node semantic rules in doc-structure governance
reading_chain:
- key: 23c_contract_node_rules
  target: 23C_CONTRACT_NODE_RULES.md
  hop: next
  reason: Contract-node rules follow the entry-node rules.
---

# 入口节点规则

## 语义审查规则
- `00_*_ENTRY.md` 只说明这个入口/步骤是干什么的，以及下一跳去哪里。
- 入口节点不应承担后续合同、实施、校验的完整正文。
- 入口节点可以条件分流，但只能分流到当前层真实可选的下一跳。
- 若当前节点只是分支索引入口，它可以只负责把读者送入若干独立叶子闭环。

## 不合格信号
- 入口页直接开始写完整规则。
- 入口页一次性列出多个深层 sibling 文档。
- 入口页承担了步骤正文或 workflow index 正文。

## 下一跳列表
- [合同节点规则]：`23C_CONTRACT_NODE_RULES.md`
- [workflow index 规则]：`23G_WORKFLOW_INDEX_RULES.md`
- [step 节点规则]：`23H_STEP_NODE_RULES.md`
- [分支索引节点规则]：`23I_BRANCH_INDEX_RULES.md`
