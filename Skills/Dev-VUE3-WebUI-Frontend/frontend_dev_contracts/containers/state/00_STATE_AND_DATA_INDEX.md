---
doc_id: "ui.dev.container.state.index"
doc_type: "ui_dev_index"
topic: "Index of container state, payload, and data-boundary contracts"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_CONTAINERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the state branch of the containers contract tree."
  - target: "10_CONTAINER_STATE_OWNERSHIP.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The ownership contract defines which container owns which state."
  - target: "20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The payload contract defines the normalization boundary and runtime bridge responsibilities."
---

# State Data Index

## 负责内容
- `10_CONTAINER_STATE_OWNERSHIP.md`
  - 定义 payload、selection、search、live status 等状态归属。
- `20_CONTAINER_PAYLOAD_NORMALIZATION.md`
  - 定义 server、bridge、容器之间的数据输入面与归一化边界。
