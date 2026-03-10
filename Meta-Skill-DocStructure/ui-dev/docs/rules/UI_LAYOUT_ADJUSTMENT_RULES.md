---
doc_id: "ui.viewer.layout_adjustment"
doc_type: "ui_dev_guide"
topic: "Layout adjustment rules for the interactive skill viewer"
anchors:
  - target: "../VIEWER_STACK_AND_REUSE.md"
    relation: "extends"
    direction: "upstream"
    reason: "Layout adjustments must extend the viewer stack contract."
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the UI development doc set."
---

# UI Layout Adjustment Rules

## 目标
- 调整布局时，优先改信息层级，不先堆视觉装饰。
- 保持 `SKILL.md` 仍是默认进入正文。
- graph、文档列表、正文面板三者必须同时可见或可快速切换，不允许把 graph 藏成二级功能。

## 调整顺序
1. 先改 `docs/` 中的布局规则。
2. 再改 `client/src/App.vue` 与相关组件。
3. 最后用真实 payload 检查节点数量、选中态与正文阅读流是否仍然清晰。

## 禁止事项
- 不要把 UI 调整知识散落回根目录文档。
- 不要让页面脱离真实 payload 改成静态演示。
- 不要为了局部视觉效果破坏文档树与 graph 的主叙事。
