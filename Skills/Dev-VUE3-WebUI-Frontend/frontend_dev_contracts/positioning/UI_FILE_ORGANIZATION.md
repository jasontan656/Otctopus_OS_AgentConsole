---
doc_id: "ui.tool.file_organization"
doc_type: "ui_dev_guide"
topic: "File organization rules for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_POSITIONING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the positioning branch."
  - target: "UI_TOOL_POSITIONING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "This guide constrains how the showroom codebase is organized."
---

# UI File Organization

## 必须留在 `ui-dev/` 的内容
- `client/` 页面与组件实现。
- `client/src/containers/` SPA 容器实现。
- `client/src/composables/` runtime bridge 与派生 view model。
- `client/src/contracts/` 容器 typed contract、layer registry 与共享前端协议类型。
- `server/` live payload server。
- `lib/` viewer payload 适配层。
- `tests/` UI runtime 相关回归。

## 必须留在 `frontend_dev_contracts/` 的内容
- 前端开发合同索引。
- `layers/` 下的 layer catalog、locator 协议与命名 lint 工作流。
- `containers/` 下的容器角色、状态边界、布局权、交互协议和治理规则。
- 组件、布局、运行链与复用边界规范。
- `rules/` 下的响应式与布局约束。

## 不应漂回 root 其他位置的内容
- 页面标题、布局细节、组件实验。
- viewer payload 组装和 service 脚本。
- `PreviewPayload` 一类 UI 语义类型。
