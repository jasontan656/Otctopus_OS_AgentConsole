---
doc_id: "ui.dev.container.layout_authority"
doc_type: "ui_dev_guide"
topic: "Layout authority boundaries for app shell, route scene, workspace, and panels"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_LAYOUT_AUTHORITY_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This contract belongs to the layout branch."
  - target: "../../rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Responsive rules refine the authority boundaries defined here."
  - target: "../model/20_CONTAINER_HIERARCHY_AND_NESTING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layout authority follows the container hierarchy."
---

# App Shell Workspace Layout Authority

## 布局裁决权
- `AppShellContainer`
  - 决定 page shell、hero、顶层信息块与场景外边距。
- `ShowroomRouteSceneContainer`
  - 决定 runtime status 区和 workspace 区的上下编排。
- `ShowroomWorkspaceContainer`
  - 决定导航栏、graph panel、reader panel 的三栏布局，以及窄屏下退化为单列顺序。
- `DocumentNavigatorContainer`
  - 只决定搜索框和文档列表内部排布。
- `GraphPanelContainer`
  - 只决定 graph 区头部与图谱画布区域分配。
- `DocumentReaderContainer`
  - 只决定正文、anchors、warning 区的内部排布。

## 裁决记录字段
- 当布局权需要被表达成可审计合同记录时，使用以下字段：
  - `action`: 例如 `layout.compose_workspace`、`layout.collapse_panel`
  - `actor_id`: 例如 `ShowroomWorkspaceContainer`
  - `scope`: 例如 `workspace.main`、`panel.reader`
  - `authz_result`: `allow` 或 `deny`
  - `deny_code`: 无权裁决时记录原因
  - `policy_version`: 当前容器布局治理版本

## 响应式退化要求
- 当视口不足以承载三栏时，由 `ShowroomWorkspaceContainer` 统一降级为单列，而不是让每个 panel 自行漂移。
- graph 仍是工作区一等公民；移动端可下沉，但不应从信息架构中消失。
