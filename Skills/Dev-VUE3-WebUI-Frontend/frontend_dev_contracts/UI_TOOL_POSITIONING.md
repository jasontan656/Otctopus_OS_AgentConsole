---
doc_id: "ui.tool.positioning"
doc_type: "ui_dev_guide"
topic: "Positioning of frontend development contracts inside Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "This guide defines how the showroom consumes the frontend contracts."
  - target: "UI_FILE_ORGANIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
---

# UI Tool Positioning

## 定位
- `frontend_dev_contracts/` 是本技能正式前端开发合同目录，不属于 `ui-dev/` 子树。
- root resident docs 和 stage docs 负责 stage 边界；`frontend_dev_contracts/` 负责沉淀稳定前端规范；`ui-dev/` 负责把规则变成可运行页面。
- 展厅是这些合同的运行消费面，不再承担合同原始存放职责。
