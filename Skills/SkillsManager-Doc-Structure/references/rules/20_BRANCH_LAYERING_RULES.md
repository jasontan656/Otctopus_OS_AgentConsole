---
doc_id: rules.branch_layering
doc_type: topic_atom
topic: Rules for layering routing branches and keeping tree depth meaningful
node_role: topic_atom
domain_type: rule_doc
anchors:
- target: 00_RULE_SYSTEM_INDEX.md
  relation: belongs_to
  direction: upstream
  reason: This rule is one branch under the rule index.
- target: 30_TREE_GRAPH_BINDING_RULES.md
  relation: feeds
  direction: downstream
  reason: Tree layering must be stable before graph binding is added.
---

# Branch Layering Rules

## 核心规则
- 分叉节点一次只承载一个分叉轴线。
- 当一个主题下的平级叶子文档过多时，应优先补一层 routing 或 index，而不是继续平铺。
- 目录层级可以继续下钻，只要每一层仍有独立语义价值。
- fewshot 示例树应故意保留足够深度，让模型能看到真实分层手法。
