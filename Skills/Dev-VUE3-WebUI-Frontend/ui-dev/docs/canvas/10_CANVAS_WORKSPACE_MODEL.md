---
doc_id: "ui.dev.docs.canvas.workspace_model"
doc_type: "topic_atom"
topic: "Canvas workspace model for showroom panels"
anchors:
  - target: "00_CANVAS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This canvas model belongs to the canvas branch."
  - target: "../../../frontend_dev_contracts/containers/interaction/10_CONTAINER_EVENT_AND_ROUTE_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The canvas model must align with the generic panel interaction protocol."
  - target: "../panels/10_SHOWROOM_PANEL_CATALOG.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Canvas lifecycle must be able to host the full panel catalog of the unified workbench."
---

# Canvas Workspace Model

## 核心原则
- Canvas is the active organization surface of the showroom.
- Every panel loaded into canvas must be closable.
- Panel open, close, and focus are workspace-level actions instead of local widget decisions.
- Canvas is responsible for co-locating document graph, code graph, AI collaboration, and reading surfaces without collapsing them into one mega panel.

## Panel 生命周期
- `openPanel`
- `focusPanel`
- `closePanel`
- `pinPanel`
- `splitPanel`
- `revealLinkedContext`

## 交互边界
- A panel may request another panel.
- A panel may not directly mutate a sibling panel.
- Canvas owns the list of open panels and their active ordering.
- Graph-originated inline jumps should open or focus the matching reader/reference panel instead of replacing the current graph surface.
- AI panels may consume the current workspace selection, but workspace state remains owned by canvas.
