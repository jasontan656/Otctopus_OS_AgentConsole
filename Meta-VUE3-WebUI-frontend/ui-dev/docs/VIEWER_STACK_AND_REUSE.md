---
doc_id: "ui.viewer.stack"
doc_type: "tooling_architecture"
topic: "Viewer stack, reusable UI direction, and showroom layout contract"
anchors:
  - target: "../UI_DEV_ENTRY.md"
    relation: "implements"
    direction: "upstream"
    reason: "This stack doc implements the ui-dev showroom entry."
  - target: "rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layout adjustment rules complement the stack contract."
---

# Viewer Stack Reuse Contract

## 技术栈
- `TypeScript`
- `Vue3`
- `Vue Flow`
- `Vite`
- `express + ws + chokidar`

## 复用方向
- 当前 viewer 是未来前端组件库与设计标准的试验母体。
- graph、文档列表、正文阅读流都是可复用的展厅母板。
- 后续组件若稳定，应从页面实现中抽离成可复用单元。
