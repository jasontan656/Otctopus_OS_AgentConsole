---
doc_id: "ui.dev.container.governance.index"
doc_type: "ui_dev_index"
topic: "Index of governance rules for SPA containers"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_CONTAINERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the governance branch of the containers contract tree."
  - target: "10_CONTAINER_PERMISSION_AND_CODE_PLACEMENT.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The governance contract defines permission visibility and code placement boundaries."
---

# Container Governance Index

## 负责内容
- `10_CONTAINER_PERMISSION_AND_CODE_PLACEMENT.md`
  - 定义容器治理范围、只读可见性边界、代码落点和测试面。
