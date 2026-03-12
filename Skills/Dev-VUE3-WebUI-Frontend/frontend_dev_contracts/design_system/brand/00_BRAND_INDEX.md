---
doc_id: "ui.dev.design_system.brand.index"
doc_type: "ui_dev_index"
topic: "Index of brand, theme, typography, and iconography contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_DESIGN_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the design-system branch."
  - target: "10_THEME_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Theme rules define the baseline showroom visual environment."
  - target: "20_BRAND_DIRECTION_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Brand-direction rules define the visual tone and accent posture."
  - target: "30_TYPOGRAPHY_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Typography rules stabilize readable hierarchy."
  - target: "40_ICONOGRAPHY_GUIDE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Iconography rules define optional visual symbols without weakening clarity."
---

# Brand Index

## 本层负责
- theme 和品牌语气
- typography 层级
- iconography 与密度规则

## 读取顺序
1. `10_THEME_GUIDE.md`
2. `20_BRAND_DIRECTION_GUIDE.md`
3. `30_TYPOGRAPHY_GUIDE.md`
4. `40_ICONOGRAPHY_GUIDE.md`
