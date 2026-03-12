---
doc_id: "ui.dev.container.hierarchy"
doc_type: "ui_dev_guide"
topic: "Hierarchy, nesting, and parent-child constraints for showroom containers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_CONTAINER_MODEL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This hierarchy contract belongs to the container model branch."
  - target: "10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The hierarchy instantiates the stable role taxonomy."
  - target: "../interaction/10_CONTAINER_EVENT_AND_ROUTE_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Parent-child topology determines allowed event flow."
---

# Container Hierarchy Nesting

## 当前推荐树形
```text
AppShellContainer
└── ShowroomRouteSceneContainer
    ├── MenuDrawerContainer
    ├── CanvasWorkspaceContainer
    │   └── CanvasPanelContainer*
    └── LocatorOverlayContainer
```

## 嵌套要求
- `AppShellContainer` 只承载顶层骨架与 scene 入口，不直接承担 panel 内容。
- `ShowroomRouteSceneContainer` 连接未来 runtime bridge、menu 与 canvas，不直接渲染具体 panel 内容。
- `MenuDrawerContainer` 只负责暴露可打开的 panel 入口，不直接拥有 panel 生命周期。
- `CanvasWorkspaceContainer` 统一拥有当前打开 panel 集合、活动 panel 顺序和共享选择态。
- `CanvasPanelContainer` 是可重复实例节点，每个实例只承载一个 panel 内容。
- graph、document library、document reader、runtime summary 都必须作为 panel 内容挂入 canvas，而不是固定挂在页面栅格里。
