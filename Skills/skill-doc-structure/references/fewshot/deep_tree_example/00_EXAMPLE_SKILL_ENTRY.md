---
doc_id: "fewshot.example.entry"
doc_type: "example_doc"
topic: "Entry node of a deep fewshot tree for a governed skill"
node_role: "entry_node"
domain_type: "fewshot"
anchors:
  - target: "../00_FEWSHOT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This example is indexed by the fewshot track entry."
  - target: "routing/10_TASK_ROUTING.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The example entry routes readers into the first routing layer."
---

# Example Skill Entry

## 作用
- 这是一个真实 fewshot 入口节点。
- 它只负责把读者送入下一层 routing。
