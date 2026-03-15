---
doc_id: skillsmanager_doc_structure.path.primary_flow.entry_node_rules
doc_type: topic_atom
topic: Entry-node semantic rules in doc-structure governance
anchors:
- target: 23A_SKILL_FACADE_RULES.md
  relation: implements
  direction: upstream
  reason: Entry-node review follows facade review.
- target: 23C_CONTRACT_NODE_RULES.md
  relation: routes_to
  direction: downstream
  reason: Contract-node rules follow the entry-node rules.
---

# 入口节点规则

## 语义审查规则
- `00_*_ENTRY.md` 只说明这个入口/步骤是干什么的，以及下一跳去哪里。
- 入口节点不应承担后续合同、实施、校验的完整正文。
- 入口节点可以条件分流，但只能分流到当前层真实可选的下一跳。

## 不合格信号
- 入口页直接开始写完整规则。
- 入口页一次性列出多个深层 sibling 文档。
- 入口页承担了步骤正文或 workflow index 正文。

## 下一跳列表
- [合同节点规则]：`23C_CONTRACT_NODE_RULES.md`
- [workflow index 规则]：`23G_WORKFLOW_INDEX_RULES.md`
- [step 节点规则]：`23H_STEP_NODE_RULES.md`
