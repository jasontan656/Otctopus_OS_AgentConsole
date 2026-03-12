---
doc_id: "ui.dev.component_system.model.index"
doc_type: "ui_dev_index"
topic: "Index of component role and API contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_COMPONENT_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the component-system branch."
  - target: "10_COMPONENT_ROLE_TAXONOMY.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Role taxonomy is the first component-model contract."
  - target: "20_COMPONENT_API_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "API contracts define the black-box input/output surface."
  - target: "30_COMPONENT_VARIANT_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Variant contracts define stable component state surfaces."
---

# Component Model Index

## 读取顺序
1. `10_COMPONENT_ROLE_TAXONOMY.md`
2. `20_COMPONENT_API_GUIDE.md`
3. `30_COMPONENT_VARIANT_GUIDE.md`
