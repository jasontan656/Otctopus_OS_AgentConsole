---
doc_id: "ui.dev.docs.purpose_boundary"
doc_type: "topic_atom"
topic: "Purpose boundary for the showroom redevelopment"
anchors:
  - target: "00_UI_DEV_DOCS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This purpose doc belongs to the showroom docs index."
  - target: "../../frontend_dev_contracts/showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The generic showroom stack contract and the showroom-specific purpose must stay aligned."
  - target: "navigation/00_NAVIGATION_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Navigation is one concrete expression of the showroom purpose."
  - target: "canvas/00_CANVAS_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Canvas workspace is the other concrete expression of the showroom purpose."
---

# Showroom Purpose Boundary

## 当前用途
- This showroom exists to make the frontend skill legible before it becomes beautiful.
- It must expose the skill structure, the frontend contracts, and the future implementation surface in one coherent SPA shell.
- It is not allowed to stay as a static three-column artifact that only mirrors old implementation accidents.

## 必须展示的内容类型
- A menu-first navigation surface for opening showroom panels.
- A canvas workspace that can host, focus, and close panels.
- Panels for graph, document browsing, document reading, runtime intent, and showroom overview.
- A clear boundary between generic frontend contracts and showroom-specific development docs.

## 非目标
- It is not a marketing landing page.
- It is not a fixed dashboard made of permanent columns.
- It is not a place to keep legacy UI code just because it still runs.
