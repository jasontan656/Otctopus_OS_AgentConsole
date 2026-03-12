---
doc_id: "ui.dev.component_system.index"
doc_type: "ui_dev_index"
topic: "Index of reusable component-system contracts for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The component-system branch is one route under the frontend development contract tree."
  - target: "model/00_COMPONENT_MODEL_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Component model contracts define roles and API/variant rules."
  - target: "packaging/00_COMPONENT_PACKAGING_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Packaging contracts define the reusable component folder shape."
  - target: "governance/00_COMPONENT_GOVERNANCE_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Governance contracts define style isolation, testing, and accessibility surfaces."
---

# Component System Index

## 本分支负责
- 定义可复用组件作为黑盒 package 的角色、职责与 API。
- 规定组件如何组合、何时复制、何时抽象、如何输出样式和 contract。
- 约束 locator、a11y、测试面如何进入组件 package。

## 读取顺序
1. `model/00_COMPONENT_MODEL_INDEX.md`
2. `packaging/00_COMPONENT_PACKAGING_INDEX.md`
3. `governance/00_COMPONENT_GOVERNANCE_INDEX.md`
