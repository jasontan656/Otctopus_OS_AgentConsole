---
doc_id: "ui.dev.container.model.index"
doc_type: "ui_dev_index"
topic: "Index of container role and hierarchy contracts"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_CONTAINERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the model branch of the containers contract tree."
  - target: "10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The taxonomy contract defines the stable role set."
  - target: "20_CONTAINER_HIERARCHY_AND_NESTING.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The hierarchy contract defines the nesting tree and parent-child restrictions."
---

# Container Model Index

## 负责内容
- `10_CONTAINER_ROLE_TAXONOMY.md`
  - 定义当前 SPA 应存在的容器角色。
- `20_CONTAINER_HIERARCHY_AND_NESTING.md`
  - 定义容器树、父子关系和禁止跨层直连的约束。
