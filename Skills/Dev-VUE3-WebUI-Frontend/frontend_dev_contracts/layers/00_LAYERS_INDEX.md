---
doc_id: "ui.dev.layers.index"
doc_type: "ui_dev_index"
topic: "Index of layer contracts, locator protocol, and UI identifier governance"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The layers branch is a top-level branch of the frontend development contract tree."
  - target: "10_LAYER_TAXONOMY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The taxonomy doc defines the fixed layer catalog."
  - target: "20_LAYER_NODE_MAPPING.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The mapping doc binds layers to concrete containers and components."
  - target: "30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The locator protocol defines the visible identifiers and global switch."
  - target: "../rules/UI_IDENTIFIER_LINT_WORKFLOW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The rules branch carries the lint workflow that enforces layer naming coverage."
---

# Layers Index

## 分支职责
- 本分支负责固定当前 skill 的 layer catalog，不把 layer 设计留给后续开发时临时新增。
- 本分支同时负责：
  - layer 全覆盖目录
  - layer-container-component 映射
  - 显式 locator 标识协议
  - 命名协议，以及通往 rules 分支的 lint 工作流入口

## 读序
- `10_LAYER_TAXONOMY.md`
- `20_LAYER_NODE_MAPPING.md`
- `30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md`
- `../rules/UI_IDENTIFIER_LINT_WORKFLOW.md`
