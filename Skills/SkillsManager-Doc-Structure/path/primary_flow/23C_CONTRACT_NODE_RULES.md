---
doc_id: skillsmanager_doc_structure.path.primary_flow.contract_node_rules
doc_type: topic_atom
topic: Contract-node semantic rules in doc-structure governance
reading_chain:
- key: 23d_tools_node_rules
  target: 23D_TOOLS_NODE_RULES.md
  hop: next
  reason: Tool-node rules follow contract-node rules.
---

# 合同节点规则

## 语义审查规则
- 合同节点只回答当前动作的目标、边界、输入输出和硬约束。
- 合同节点不应提前展开工具清单、实施细节或最终校验细节。
- 若约束只属于当前动作，应放在这里；若只属于后续动作，应继续下沉。

## 不合格信号
- 合同页混入命令大全。
- 合同页开始展开完整实施流程。
- 合同页承担后续步骤的局部规则。

## 下一跳列表
- [tool/lint 节点规则]：`23D_TOOLS_NODE_RULES.md`
