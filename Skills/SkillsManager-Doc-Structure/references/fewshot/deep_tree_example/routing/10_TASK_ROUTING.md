---
doc_id: fewshot.example.task_routing
doc_type: routing_doc
topic: First routing layer of the deep fewshot tree
node_role: routing_doc
domain_type: fewshot
anchors:
- target: ../00_EXAMPLE_SKILL_ENTRY.md
  relation: belongs_to
  direction: upstream
  reason: This routing doc belongs to the example entry.
- target: restructure/20_ARCHITECTURE_ROUTING.md
  relation: routes_to
  direction: downstream
  reason: This branch continues into the restructure path.
---

# Task Routing

## 当前分叉
- 这里只承担一个轴线：当前任务进入哪一条治理路径。
