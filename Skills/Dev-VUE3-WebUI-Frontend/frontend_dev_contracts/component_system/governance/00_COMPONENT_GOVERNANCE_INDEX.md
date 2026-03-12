---
doc_id: "ui.dev.component_system.governance.index"
doc_type: "ui_dev_index"
topic: "Index of component governance contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_COMPONENT_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the component-system branch."
  - target: "10_COMPONENT_STYLE_ISOLATION.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Style isolation is the first governance contract."
  - target: "20_COMPONENT_TEST_SURFACE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Testing surfaces stabilize component quality."
  - target: "30_COMPONENT_ACCESSIBILITY_SURFACE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Accessibility surfaces define the non-visual usability contract."
---

# Component Governance Index

## 读取顺序
1. `10_COMPONENT_STYLE_ISOLATION.md`
2. `20_COMPONENT_TEST_SURFACE.md`
3. `30_COMPONENT_ACCESSIBILITY_SURFACE.md`
