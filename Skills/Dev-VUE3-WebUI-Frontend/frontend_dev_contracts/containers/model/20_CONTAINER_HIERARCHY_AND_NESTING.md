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
    ├── RuntimeStatusContainer
    └── ShowroomWorkspaceContainer
        ├── DocumentNavigatorContainer
        ├── GraphPanelContainer
        └── DocumentReaderContainer
```

## 嵌套要求
- `AppShellContainer` 只承载顶层页面骨架与 route scene 入口，不直接拥有文档筛选或正文渲染逻辑。
- `ShowroomRouteSceneContainer` 连接 runtime bridge 与 workspace，不直接承担 graph 节点渲染。
- `ShowroomWorkspaceContainer` 作为工作区级父容器，拥有当前选中文档路径和搜索关键字。
- `DocumentNavigatorContainer`、`GraphPanelContainer`、`DocumentReaderContainer` 都从工作区读取共享选择态，不允许兄弟容器直接改写彼此内部状态。
- `RuntimeStatusContainer` 读取 runtime 摘要，但不控制 workspace 布局。
