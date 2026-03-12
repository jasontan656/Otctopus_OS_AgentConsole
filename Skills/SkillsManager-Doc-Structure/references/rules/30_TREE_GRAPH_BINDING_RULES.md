---
doc_id: "rules.tree_graph_binding"
doc_type: "topic_atom"
topic: "Rules for binding graph cross-links onto a stable primary tree"
node_role: "topic_atom"
domain_type: "rule_doc"
anchors:
  - target: "00_RULE_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This rule is one branch under the rule index."
  - target: "../metadata/30_ANCHOR_WRITING_CONTRACT.md"
    relation: "details"
    direction: "downstream"
    reason: "Anchor-writing rules expand how graph bindings should be written."
---

# Tree Graph Binding Rules

## 核心规则
- tree 是主路径，graph 是补充路径。
- anchors 应优先表达 `upstream/downstream` 主路径，再补 `cross/lateral` 关系。
- cross-links 可以跨层，但不能让读者失去“当前处于哪条主路径”的判断。
