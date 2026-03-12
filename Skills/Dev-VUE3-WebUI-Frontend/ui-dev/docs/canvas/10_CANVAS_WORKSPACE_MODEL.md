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
---

# Canvas Workspace Model

## 核心原则
- Canvas is the active organization surface of the showroom.
- Every panel loaded into canvas must be closable.
- Panel open, close, and focus are workspace-level actions instead of local widget decisions.

## Panel 生命周期
- `openPanel`
- `focusPanel`
- `closePanel`

## 交互边界
- A panel may request another panel.
- A panel may not directly mutate a sibling panel.
- Canvas owns the list of open panels and their active ordering.
