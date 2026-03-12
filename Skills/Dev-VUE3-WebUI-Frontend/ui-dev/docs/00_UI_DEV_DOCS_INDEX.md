---
doc_id: "ui.dev.docs.index"
doc_type: "index_doc"
topic: "Index of showroom-specific development docs for Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the first branch below the ui-dev entry."
  - target: "10_SHOWROOM_PURPOSE_AND_SCOPE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Showroom purpose and scope is the first showroom-specific document."
  - target: "domains/00_GOVERNANCE_DOMAIN_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Domain docs define how the unified workbench distinguishes and renders governed sources."
  - target: "navigation/00_NAVIGATION_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Navigation docs define the SPA menu surface."
  - target: "canvas/00_CANVAS_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Canvas docs define the workspace and panel lifecycle."
  - target: "panels/00_PANEL_CATALOG_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Panel docs define what the showroom should actually contain."
  - target: "../../frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The showroom docs complement the generic frontend contract tree."
---

# UI Dev Docs Index

## 本分支负责
- `10_SHOWROOM_PURPOSE_AND_SCOPE.md`
  - 定义这个展厅的用途边界和展示范围。
- `domains/00_GOVERNANCE_DOMAIN_INDEX.md`
  - 定义多治理域如何在同一个 workbench 中被发现、区分和渲染。
- `navigation/00_NAVIGATION_INDEX.md`
  - 定义 SPA 菜单导航、可展开入口与菜单分组。
- `canvas/00_CANVAS_INDEX.md`
  - 定义 canvas workspace、panel 生命周期与关闭交互。
- `panels/00_PANEL_CATALOG_INDEX.md`
  - 定义展厅必须包含哪些 panel，以及每个 panel 的用途。

## 读取顺序
1. `10_SHOWROOM_PURPOSE_AND_SCOPE.md`
2. `domains/00_GOVERNANCE_DOMAIN_INDEX.md`
3. `navigation/00_NAVIGATION_INDEX.md`
4. `canvas/00_CANVAS_INDEX.md`
5. `panels/00_PANEL_CATALOG_INDEX.md`
