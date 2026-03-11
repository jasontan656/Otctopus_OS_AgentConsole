---
doc_id: "rules.entry_handoff"
doc_type: "topic_atom"
topic: "Rules for handing readers from the entry node into the document tree"
node_role: "topic_atom"
domain_type: "rule_doc"
anchors:
  - target: "00_RULE_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This rule is one branch under the rule index."
  - target: "20_BRANCH_LAYERING_RULES.md"
    relation: "feeds"
    direction: "downstream"
    reason: "Entry handoff rules determine how the next branch layers should be built."
---

# Entry Handoff Rules

## 核心规则
- 文档树必须把入口节点当作稳定起点。
- 入口节点之后优先进入分叉节点或索引节点，而不是直接把所有叶子文档平铺到顶层。
- 入口节点在本技能中承担 tree root 与 first handoff 角色。
