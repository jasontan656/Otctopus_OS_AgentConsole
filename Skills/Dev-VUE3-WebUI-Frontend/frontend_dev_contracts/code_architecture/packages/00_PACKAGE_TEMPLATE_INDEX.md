---
doc_id: "ui.dev.code_architecture.package_template.index"
doc_type: "ui_dev_index"
topic: "Index of component package template and style placement contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_CODE_ARCHITECTURE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the code-architecture branch."
  - target: "10_COMPONENT_FOLDER_TEMPLATE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The component folder template is the primary package template contract."
  - target: "20_STYLE_ASSET_PLACEMENT.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Style asset placement defines how global and local styles coexist."
  - target: "30_COMPONENT_EXPORT_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Export rules define the package entry discipline."
  - target: "40_COMPONENT_REGISTRY_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Registry rules define the package-to-registry synchronization contract."
---

# Package Template Index

## 读取顺序
1. `10_COMPONENT_FOLDER_TEMPLATE.md`
2. `20_STYLE_ASSET_PLACEMENT.md`
3. `30_COMPONENT_EXPORT_GUIDE.md`
4. `40_COMPONENT_REGISTRY_GUIDE.md`
