---
doc_id: "ui.dev.code_architecture.index"
doc_type: "ui_dev_index"
topic: "Index of frontend code architecture contracts for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The code-architecture branch is one route under the frontend development contract tree."
  - target: "topology/00_TOPOLOGY_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Topology contracts define the high-level frontend folder layout and dependency direction."
  - target: "packages/00_PACKAGE_TEMPLATE_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Package template contracts define the folder-first component package layout."
  - target: "governance/00_CODE_GOVERNANCE_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Governance contracts define copy/reuse and export discipline."
---

# Code Architecture Index

## 本分支负责
- `ui-dev/client/src` 的目录拓扑
- container / component / composable / contract / styles / tokens 的依赖方向
- 组件 package 模板与导出规则
- 样式资产的全局/局部落点

## 读取顺序
1. `topology/00_TOPOLOGY_INDEX.md`
2. `packages/00_PACKAGE_TEMPLATE_INDEX.md`
3. `governance/00_CODE_GOVERNANCE_INDEX.md`
