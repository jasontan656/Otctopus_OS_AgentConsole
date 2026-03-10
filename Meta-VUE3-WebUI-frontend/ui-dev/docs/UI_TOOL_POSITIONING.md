---
doc_id: "ui.tool.positioning"
doc_type: "ui_dev_guide"
topic: "Positioning of the ui-dev showroom inside Meta-VUE3-WebUI-frontend"
anchors:
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the ui-dev showroom root."
  - target: "UI_FILE_ORGANIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
---

# UI Tool Positioning

## 定位
- `ui-dev/` 是前端实现与展示层，不是 stage contracts 的来源。
- root resident docs 和 stage docs 负责规则；`ui-dev/` 负责把规则变成可运行页面。
- 这个页面既是开发载体，也是人类理解 graph 的展厅。
