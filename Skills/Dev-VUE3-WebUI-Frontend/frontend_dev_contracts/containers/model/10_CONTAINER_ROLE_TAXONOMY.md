---
doc_id: "ui.dev.container.role_taxonomy"
doc_type: "ui_dev_guide"
topic: "Stable taxonomy for SPA containers in the Vue showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_CONTAINER_MODEL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This taxonomy belongs to the container model branch."
  - target: "../state/10_CONTAINER_STATE_OWNERSHIP.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Role semantics must match state ownership boundaries."
  - target: "../layout/10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Container roles imply different layout authority scopes."
---

# Container Role Taxonomy

## 当前 skill 的稳定容器角色
- `AppShellContainer`
  - 承载全局页面壳层、hero、顶层状态卡和整体页面语义。
- `ShowroomRouteSceneContainer`
  - 承载 showroom 这条 route scene 的单入口，不直接承担 graph 或 reader 内部细节。
- `ShowroomWorkspaceContainer`
  - 承载文档导航、graph、正文阅读三大工作区面板，并持有工作区级选择态。
- `DocumentNavigatorContainer`
  - 承载文档检索、筛选和当前文档选择入口。
- `GraphPanelContainer`
  - 承载 anchor graph 展示和节点选择输入，不拥有全局 payload。
- `DocumentReaderContainer`
  - 承载正文阅读、incoming/outgoing anchors、atomicity warnings。
- `RuntimeStatusContainer`
  - 承载 live status、graph status、doc/edge 数量等运行态摘要。
- `ShowroomRuntimeBridge`
  - 承载 `/api/preview` 和 `/live` 的 runtime 桥接、payload 刷新与错误退化，不直接决定页面布局。

## 角色约束
- 图谱渲染组件例如 `GraphCanvas` 属于展示组件，不上升为拥有业务状态的容器。
- 容器角色的划分依据是状态所有权、布局权和交互协议，不是视觉盒子数量。
- 单个容器应只有一个主责任；若同时承担 route、payload、workspace 编排、panel 细节，应继续拆分。
