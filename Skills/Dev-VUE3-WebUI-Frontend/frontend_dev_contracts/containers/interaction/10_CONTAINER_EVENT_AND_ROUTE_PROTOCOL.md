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
- `ShowroomWorkspaceContainer` 从 scene 接收 `payload`，并向下分发只读 docs、edges、selectedDoc。

## 输出协议
- `DocumentNavigatorContainer` 发出：
  - `updateSearch(keyword)`
  - `selectDoc(path)`
- `GraphPanelContainer` 发出：
  - `selectDoc(path)`
- `DocumentReaderContainer` 发出：
  - `followAnchor(path)`

## 协议约束
- 兄弟容器之间不直接互改状态。
- 当前 viewer 尚未把选中路径编码进 URL；因此 route scene 负责场景入口，但具体选择协议仍由 workspace 统一裁决。
