---
doc_id: "ui.dev.docs.index"
doc_type: "ui_dev_index"
topic: "Index of frontend development contracts for Dev-VUE3-WebUI-Frontend"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "The showroom consumes this frontend contract index as its official reading path."
  - target: "../ui-dev/docs/00_UI_DEV_DOCS_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Showroom-specific development docs complement the generic frontend contract tree."
  - target: "design_system/00_DESIGN_SYSTEM_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Design-system contracts define tokens, semantic styles, theming, and typography."
  - target: "component_system/00_COMPONENT_SYSTEM_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Component-system contracts define reusable black-box component packages and API rules."
  - target: "code_architecture/00_CODE_ARCHITECTURE_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Code-architecture contracts define folder topology, dependency direction, and package shape placement."
  - target: "layers/00_LAYERS_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Layer contracts define the long-lived layer catalog, node mapping, locator protocol, and lint workflow."
  - target: "containers/00_CONTAINERS_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Container contracts define the SPA shell, workspace, state, and governance boundaries."
  - target: "positioning/00_POSITIONING_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Positioning and file-boundary contracts form the first branch of the frontend contract tree."
  - target: "showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Showroom runtime contracts form the second branch of the frontend contract tree."
  - target: "rules/00_RULES_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Layout and responsive rules form the rule branch of the frontend contract tree."
---

# Frontend Development Contracts

## 分支读序
- `design_system/00_DESIGN_SYSTEM_INDEX.md`
  - 负责 design tokens、语义样式映射、theme/brand、typography 与 iconography。
- `component_system/00_COMPONENT_SYSTEM_INDEX.md`
  - 负责可复用黑盒组件的角色、API、变体、style isolation 与测试面。
- `code_architecture/00_CODE_ARCHITECTURE_INDEX.md`
  - 负责 folder topology、组件 package 模板、依赖方向、style 资产落点与导出规则。
- `layers/00_LAYERS_INDEX.md`
  - 负责 layer 全覆盖设计、layer-container-component 映射、locator 协议与 lint 工作流。
- `containers/00_CONTAINERS_INDEX.md`
  - 负责 SPA 容器角色、层级、状态边界、布局权、交互协议与治理规则。
- `positioning/00_POSITIONING_INDEX.md`
  - 负责合同定位、目录边界、文件组织。
- `showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md`
  - 负责 SPA menu/canvas 目标、showroom runtime 恢复门禁与未来运行链。
- `rules/00_RULES_INDEX.md`
  - 负责布局调整与响应式约束。
- `../ui-dev/docs/00_UI_DEV_DOCS_INDEX.md`
  - 负责这个 showroom 自己要展示什么、菜单怎么组织、canvas 怎么承载 panel。

## 最小读取路径
1. 先读 `design_system/00_DESIGN_SYSTEM_INDEX.md`，确认 tokens、语义样式和主题基线。
2. 再读 `component_system/00_COMPONENT_SYSTEM_INDEX.md`，确认组件 black-box 包形状和 API 约束。
3. 再读 `code_architecture/00_CODE_ARCHITECTURE_INDEX.md`，确认代码目录、样式资产和导出落点。
4. 再读 `layers/00_LAYERS_INDEX.md`，确认 layer catalog、节点命名协议和 locator 治理边界。
5. 再读 `containers/00_CONTAINERS_INDEX.md`，确认 SPA 容器树、状态边界和布局权边界。
6. 再读 `positioning/00_POSITIONING_INDEX.md`，确认这个目录在整个 skill 里的职责。
7. 再读 `showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md`，确认展厅运行面和复用面。
8. 最后读 `rules/00_RULES_INDEX.md`，收敛到具体 lint 和布局规则。
