---
doc_id: "stages.showroom_runtime"
doc_type: "stage_doc"
topic: "Runnable showroom and runtime delivery stage for the Vue3 web UI frontend skill"
anchors:
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "implements"
    direction: "downstream"
    reason: "The runnable showroom root is the concrete execution surface of this stage."
  - target: "../../frontend_dev_contracts/layers/30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "The locator protocol defines the visible node identifiers that the runtime UI must surface."
  - target: "../../frontend_dev_contracts/containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "details"
    direction: "downstream"
    reason: "The payload normalization contract defines the runtime bridge input boundary for the showroom."
  - target: "../../frontend_dev_contracts/rules/UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "details"
    direction: "downstream"
    reason: "The runtime stage also enforces component package shape and export discipline."
  - target: "../../references/tooling/development/modules/mod_showroom_runtime.md"
    relation: "explained_by"
    direction: "downstream"
    reason: "The showroom runtime module documents server, viewer, and service responsibilities."
---

# Stage Showroom Runtime

## 本阶段负责
- 定义 showroom 自身的用途、菜单导航、canvas 工作区与 panel catalog。
- 保持 `ui-dev/` 作为 showroom redevelopment docs root，而不是保留一套已经偏离目标的旧 UI 代码。
- 让人类先通过文档确认展厅应该展示什么，再进入下一轮代码重建。
- 保留未来 runtime bridge、workspace 容器、panel 容器与 locator 协议的目标叙事，但不假装当前已经落地。

## 交付要求
- `ui-dev/UI_DEV_ENTRY.md` 成为 showroom docs 的稳定入口。
- `ui-dev/docs/` 明确说明 SPA menu、canvas workspace、panel catalog 与语言规则。
- 当前 skill 内不再保留会误导读者的旧 runnable UI 代码与依赖。
