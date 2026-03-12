---
doc_id: "ui.dev.code_architecture.topology.index"
doc_type: "ui_dev_index"
topic: "Index of frontend folder topology and dependency direction contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_CODE_ARCHITECTURE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the code-architecture branch."
  - target: "10_FRONTEND_FOLDER_TOPOLOGY.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Folder topology is the first architecture contract."
  - target: "20_DEPENDENCY_DIRECTION_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Dependency direction prevents architecture drift."
---

# Topology Index

## 读取顺序
1. `10_FRONTEND_FOLDER_TOPOLOGY.md`
2. `20_DEPENDENCY_DIRECTION_GUIDE.md`
