---
doc_id: "ui.dev.container.interaction.index"
doc_type: "ui_dev_index"
topic: "Index of interaction and route protocols for SPA containers"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_CONTAINERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the interaction branch of the containers contract tree."
  - target: "10_CONTAINER_EVENT_AND_ROUTE_PROTOCOL.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The interaction contract defines event flow between workspace containers."
---

# Interaction Protocol Index

## 负责内容
- `10_CONTAINER_EVENT_AND_ROUTE_PROTOCOL.md`
  - 定义 runtime bridge、workspace、panel 之间的输入输出协议。
