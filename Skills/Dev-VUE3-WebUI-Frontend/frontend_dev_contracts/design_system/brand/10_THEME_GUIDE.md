---
doc_id: "ui.dev.design_system.theme_guide"
doc_type: "ui_dev_guide"
topic: "Theme guide for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_BRAND_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Theme rules belong to the brand branch."
---

# Theme Guide

## 当前主题方向
- daylight editorial showroom
  - 明亮、空气感、阅读优先。
  - 暖色 accent + 冷色 runtime/graph 辅助。
- 不走默认紫白模板，也不默认深色模式。

## 主题约束
- 页面背景允许使用多层渐变与柔和 radial atmosphere，但仍必须保持正文可读性。
- hero 与 panel 采用统一玻璃感/纸感混合表面，不允许每块面板各自发明材质。
- selected / focus / highlight 必须共享同一 accent 系统。
