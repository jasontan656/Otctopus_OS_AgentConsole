---
doc_id: "ui.dev.container.interaction_protocol"
doc_type: "ui_dev_guide"
topic: "Event, selection, and route-scene protocol for showroom containers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_INTERACTION_PROTOCOL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This protocol belongs to the interaction branch."
  - target: "../state/20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Interaction begins from normalized runtime payload."
  - target: "../model/20_CONTAINER_HIERARCHY_AND_NESTING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Allowed event flow depends on the container tree."
---

# Container Event Route Protocol

## 输入协议
- `ShowroomRouteSceneContainer` 从 runtime bridge 接收 `payload` 与 `liveState`。
- `CanvasWorkspaceContainer` 从 scene 接收 `payload`，并统一裁决 panel open / close / focus / select。

## 输出协议
- `MenuDrawerContainer` 发出：
  - `openPanel(panelKind)`
  - `toggleMenu()`
- `CanvasPanelContainer` 发出：
  - `focusPanel(panelId)`
  - `closePanel(panelId)`
- panel 内容发出：
  - `selectDoc(path)`
  - `followAnchor(path)`
  - `requestPanel(panelKind)`

## 协议约束
- 兄弟容器之间不直接互改状态。
- 任何 panel 的打开、关闭和活动态切换都必须经过 `CanvasWorkspaceContainer`。
- 当前 showroom 仍未把 panel 状态编码进 URL；因此 scene 负责入口，workspace 负责交互裁决。
