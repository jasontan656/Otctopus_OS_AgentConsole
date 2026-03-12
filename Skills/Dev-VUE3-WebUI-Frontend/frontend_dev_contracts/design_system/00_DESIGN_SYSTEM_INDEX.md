---
doc_id: "ui.dev.design_system.index"
doc_type: "ui_dev_index"
topic: "Index of design-system contracts for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The design-system branch is one route under the frontend development contract tree."
  - target: "foundations/00_FOUNDATIONS_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Foundations define tokens and semantic style mapping."
  - target: "brand/00_BRAND_INDEX.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Brand contracts define theme, typography, iconography, and visual tone."
  - target: "../component_system/00_COMPONENT_SYSTEM_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Component-system contracts consume the design-system tokens and semantic styles."
---

# Design System Index

## 本分支负责
- 为整个 `ui-dev/` 提供统一的 token、语义样式名和主题约束。
- 规定容器与组件只能消费语义 token，不允许在实现面随意写死颜色、阴影、圆角、间距和字体。
- 为 showroom 当前视觉风格与未来扩展组件库提供同一套设计语言。

## 读取顺序
1. `foundations/00_FOUNDATIONS_INDEX.md`
2. `brand/00_BRAND_INDEX.md`

## 产出约束
- token 必须能被全局样式和局部组件 package 共同消费。
- semantic style 名必须稳定，不能直接暴露业务页面临时命名。
- typography、iconography 和 theme 切换规则必须能指导实际 UI 重构。
