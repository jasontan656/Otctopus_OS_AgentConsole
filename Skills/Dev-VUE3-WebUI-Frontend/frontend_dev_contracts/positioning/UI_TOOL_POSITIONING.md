---
doc_id: "ui.tool.positioning"
doc_type: "ui_dev_guide"
topic: "Positioning of frontend development contracts inside Dev-VUE3-WebUI-Frontend"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_POSITIONING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the positioning branch."
  - target: "SCREEN_SPATIAL_BLUEPRINT_CONTRACT.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Spatial blueprints are the concrete layout-planning carrier under positioning governance."
  - target: "../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "supports"
    direction: "upstream"
    reason: "This guide defines how product-runtime handoff consumes the frontend contracts."
  - target: "UI_FILE_ORGANIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
---

# UI Tool Positioning

## 定位
- `frontend_dev_contracts/` 是本技能正式前端开发合同目录，只承载稳定前端规范与 handoff 规则。
- root resident docs 和 stage docs 负责 stage 边界；`frontend_dev_contracts/` 负责沉淀稳定前端规范；具体产品运行时需求与产品代码必须落在产品仓。
- 本技能只定义“如何交接给产品运行时”，不再保存产品级界面目录。
- 当布局已经涉及多容器、多 panel、多 graph viewport 或复杂挤压关系时，必须先使用 `SCREEN_SPATIAL_BLUEPRINT_CONTRACT.md` 把空间结构落成蓝图，再进入产品实现。
