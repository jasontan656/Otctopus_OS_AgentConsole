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
  - target: "../domains/10_UNIFIED_GOVERNANCE_WORKBENCH_MODEL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Navigation groups must reflect the workbench domain model instead of ad hoc pages."
---

# Menu Navigation Model

## 导航原则
- Navigation must be menu-first instead of column-first.
- The menu must be expandable and collapsible.
- The menu must open panels into the canvas workspace instead of acting as a permanent content column.
- The menu must surface governance-domain boundaries before it surfaces leaf content.
- The menu may discover concrete doc packs and repo entries at runtime, but the group taxonomy must stay stable.

## 菜单分组
- `Workbench`
- `Governance Domains`
- `Documents`
- `Code Graph`
- `AI Workspace`
- `Runtime`

## 菜单动作
- Open a panel into canvas.
- Focus an existing panel if it is already open.
- Collapse or expand the menu without changing canvas state.
- Expand one governance domain and lazily load its discoverable entries.
- Offer inline jump actions from one domain panel to another without forcing a full route switch.
