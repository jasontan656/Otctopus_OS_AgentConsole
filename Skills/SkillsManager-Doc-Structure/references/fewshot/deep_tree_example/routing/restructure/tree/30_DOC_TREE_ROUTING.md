---
doc_id: fewshot.example.doc_tree_routing
doc_type: routing_doc
topic: Third routing layer of the deep fewshot tree
node_role: routing_doc
domain_type: fewshot
anchors:
- target: ../20_ARCHITECTURE_ROUTING.md
  relation: belongs_to
  direction: upstream
  reason: This routing doc belongs to the architecture-routing layer.
- target: atoms/40_SINGLE_DOC_AUTHORING.md
  relation: routes_to
  direction: downstream
  reason: This branch narrows into a single-doc authoring atom.
---

# Doc Tree Routing

## 当前分叉
- 这里只承担一个轴线：当前进入哪一类文档树子任务。
