---
doc_id: "ui.dev.component_system.packaging.index"
doc_type: "ui_dev_index"
topic: "Index of reusable component package-shape contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_COMPONENT_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the component-system branch."
  - target: "10_COMPONENT_PACKAGE_SHAPE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Package shape is the primary packaging rule."
  - target: "20_COMPONENT_COMPOSITION_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Composition rules control how packages can be assembled."
  - target: "30_COMPONENT_REUSE_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Reuse policy defines when packages should be reused or copied."
---

# Component Packaging Index

## 读取顺序
1. `10_COMPONENT_PACKAGE_SHAPE.md`
2. `20_COMPONENT_COMPOSITION_GUIDE.md`
3. `30_COMPONENT_REUSE_GUIDE.md`
