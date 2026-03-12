---
doc_id: "ui.dev.docs.navigation.menu_model"
doc_type: "topic_atom"
topic: "Expandable SPA menu model for the showroom"
anchors:
  - target: "00_NAVIGATION_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This menu model belongs to the navigation branch."
  - target: "../../../frontend_dev_contracts/containers/layout/10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The menu model must align with the generic layout-authority contract."
---

# Menu Navigation Model

## 导航原则
- Navigation must be menu-first instead of column-first.
- The menu must be expandable and collapsible.
- The menu must open panels into the canvas workspace instead of acting as a permanent content column.

## 菜单分组
- `Overview`
- `Explore`
- `Documents`
- `Runtime`

## 菜单动作
- Open a panel into canvas.
- Focus an existing panel if it is already open.
- Collapse or expand the menu without changing canvas state.
