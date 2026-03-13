---
doc_id: fewshot.example.architecture_routing
doc_type: routing_doc
topic: Second routing layer of the deep fewshot tree
node_role: routing_doc
domain_type: fewshot
anchors:
- target: ../10_TASK_ROUTING.md
  relation: belongs_to
  direction: upstream
  reason: This routing doc belongs to the task-routing layer.
- target: tree/30_DOC_TREE_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: This branch continues into the document-tree layer.
---

# Architecture Routing

## 当前分叉
- 这里只承担一个轴线：当前是否进入文档树架构治理。
