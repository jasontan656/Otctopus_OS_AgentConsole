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
  - target: "../../positioning/SCREEN_SPATIAL_BLUEPRINT_CONTRACT.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layout authority decides who has placement power; spatial blueprints describe the concrete placement."
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
  - 决定 page shell、顶层品牌区、菜单入口位置与 canvas 外边距。
- `ShowroomRouteSceneContainer`
  - 决定 menu drawer、canvas workspace 与 overlay 的场景级编排。
- `MenuDrawerContainer`
  - 只决定菜单折叠态、展开态与 section 组织，不直接拥有 canvas 内部布局权。
- `CanvasWorkspaceContainer`
  - 决定 panel 在 canvas 中的排列、活动态与空态。
- `CanvasPanelContainer`
  - 只决定单个 panel header、close affordance 和 panel body 的内部排布。

## 裁决记录字段
- 当布局权需要被表达成可审计合同记录时，使用以下字段：
  - `action`: 例如 `layout.compose_workspace`、`layout.collapse_panel`
  - `actor_id`: 例如 `ShowroomWorkspaceContainer`
  - `scope`: 例如 `workspace.main`、`panel.reader`
  - `authz_result`: `allow` 或 `deny`
  - `deny_code`: 无权裁决时记录原因
  - `policy_version`: 当前容器布局治理版本

## 响应式退化要求
- 当视口不足以同时承载 menu 与 canvas 时，由 `ShowroomRouteSceneContainer` 统一把菜单切成 overlay drawer。
- canvas 中的 panel 可以改变排列，但不能退化成固定三栏遗留布局。

## 与 spatial blueprint 的关系
- 本文定义“谁有权摆放”。
- `SCREEN_SPATIAL_BLUEPRINT_CONTRACT.md` 定义“摆在哪里、占多大、谁挤压谁、谁覆盖谁”。
- 复杂界面不能只写 authority 而没有 blueprint；否则模型无法推理屏幕空间结果。
