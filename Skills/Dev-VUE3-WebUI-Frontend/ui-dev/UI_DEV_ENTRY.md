---
doc_id: "ui.dev.entry"
doc_type: "ui_dev_entry"
topic: "Showroom redevelopment root for Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The ui-dev root is the concrete surface of the showroom redevelopment stage."
  - target: "../frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The frontend contract index defines the official UI development reading path."
  - target: "docs/00_UI_DEV_DOCS_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The ui-dev docs index defines the showroom-specific purpose, menu, canvas, and panel scope."
  - target: "../frontend_dev_contracts/design_system/00_DESIGN_SYSTEM_INDEX.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "The showroom docs must stay aligned with the generic design-system contracts."
  - target: "../frontend_dev_contracts/component_system/00_COMPONENT_SYSTEM_INDEX.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "The future showroom implementation must stay aligned with the generic component-system contracts."
  - target: "../frontend_dev_contracts/code_architecture/00_CODE_ARCHITECTURE_INDEX.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "The future showroom implementation must stay aligned with the generic code-architecture contracts."
  - target: "../frontend_dev_contracts/layers/00_LAYERS_INDEX.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "The future showroom implementation must stay aligned with the generic layer catalog and locator protocol."
---

# UI Dev Entry

`ui-dev/` 是本技能的 showroom redevelopment 根目录。当前这里不再保留旧 runnable UI 代码，而是只保留门面入口与展厅自身开发文档。

## 包含内容
- `docs/00_UI_DEV_DOCS_INDEX.md`
  - showroom 自身开发文档入口。
- `docs/10_SHOWROOM_PURPOSE_AND_SCOPE.md`
  - 定义这个展厅要展示什么、不展示什么。
- `docs/domains/`
  - 定义多治理域如何在同一个 workbench 中被识别、发现和渲染。
- `docs/navigation/`
  - 定义 SPA 菜单导航与可扩展入口。
- `docs/canvas/`
  - 定义 canvas workspace、panel 生命周期与关闭交互。
- `docs/panels/`
  - 定义应该存在的 panel catalog。
- `frontend_dev_contracts/`
  - 继续承载通用前端规则，不承担 showroom 自身的内容目录。

## 使用方式
- 当前读取方式：
  1. 先读 `docs/00_UI_DEV_DOCS_INDEX.md`
  2. 再回到 `../frontend_dev_contracts/00_UI_DEVELOPMENT_INDEX.md` 对齐通用合同
- 当任务落到统一工作台目标定义时，应优先读 `docs/domains/` 与 `docs/panels/`，避免把“单一 showroom”假设带入 runtime 设计。
- 只有当新的 UI 代码被重建后，`ui-dev/` 才会重新恢复 dev/build/runtime 入口。
