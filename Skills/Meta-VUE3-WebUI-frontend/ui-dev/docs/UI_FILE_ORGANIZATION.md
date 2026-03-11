---
doc_id: "ui.tool.file_organization"
doc_type: "ui_dev_guide"
topic: "File organization rules for the Meta-VUE3-WebUI-frontend showroom"
anchors:
  - target: "UI_TOOL_POSITIONING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This file-organization guide belongs to the ui-dev root."
---

# UI File Organization

## 必须留在 `ui-dev/` 的内容
- `client/` 页面与组件实现。
- `server/` live payload server。
- `lib/` viewer payload 适配层。
- `tests/` UI runtime 相关回归。
- `docs/` UI 开发文档。

## 不应漂回 root 的内容
- 页面标题、布局细节、组件实验。
- viewer payload 组装和 service 脚本。
- `PreviewPayload` 一类 UI 语义类型。
