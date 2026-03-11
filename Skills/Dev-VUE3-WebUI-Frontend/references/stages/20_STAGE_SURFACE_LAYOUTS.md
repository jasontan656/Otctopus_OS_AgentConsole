---
doc_id: "stages.surface_layouts"
doc_type: "stage_doc"
topic: "Responsive surface rules for desktop, mobile landscape, and mobile portrait"
anchors:
  - target: "../../ui-dev/docs/rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "implements"
    direction: "downstream"
    reason: "Runtime layout adjustments must follow these surface rules."
  - target: "30_STAGE_MOTION_COMPONENT_ARCHITECTURE.md"
    relation: "feeds"
    direction: "downstream"
    reason: "Surface choices constrain later motion and component organization."
---

# Stage Surface Layouts

## 设备面规范
- `desktop`：三栏叙事完整展开，graph 与正文同时可见。
- `mobile_landscape`：保留 graph 主位，列表与正文采用更紧凑切换。
- `mobile_portrait`：优先保留当前节点上下文，不牺牲 graph 的可追踪性。

## 核心要求
- graph、文档索引、正文面板必须同时可见或可快速切换。
- 不允许把 graph 藏成二级入口。
- 响应式不是缩放版桌面，而是重组叙事顺序。
