---
doc_id: skillsmanager_doc_structure.path.primary_flow.tools_node_rules
doc_type: topic_atom
topic: Tool or lint-node semantic rules in doc-structure governance
reading_chain:
- key: 23e_execution_node_rules
  target: 23E_EXECUTION_NODE_RULES.md
  hop: next
  reason: Execution-node rules follow tool-node rules.
---

# Tool/Lint 节点规则

## 语义审查规则
- `15_TOOLS.md` 承载当前节点自己的工具或 lint 能力面。
- 即使当前节点只有 lint，没有额外工具，也仍可在该节点写清楚检查入口。
- 该节点不应承担完整实施步骤和最终校验结论。

## 不合格信号
- 把其他入口的工具说明混进当前节点。
- 工具页直接承担完整执行正文。
- 用工具页重新集中全技能所有命令。

## 下一跳列表
- [执行节点规则]：`23E_EXECUTION_NODE_RULES.md`
