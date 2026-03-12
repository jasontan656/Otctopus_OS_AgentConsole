---
doc_id: "ui.dev.design_system.typography_guide"
doc_type: "ui_dev_guide"
topic: "Typography guide for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_BRAND_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Typography rules belong to the brand branch."
  - target: "../../component_system/governance/30_COMPONENT_ACCESSIBILITY_SURFACE.md"
    relation: "supports"
    direction: "cross"
    reason: "Readable type hierarchy is part of accessibility-surface governance."
---

# Typography Guide

## 字体层级
- display
  - hero 主标题。
- title
  - panel 标题、文档标题。
- body
  - 正文、说明文、legend 文本。
- meta
  - timestamp、路径、辅助说明。
- code
  - 路径、id、locator、monospace 信息。

## 规则
- 标题与正文必须使用不同字重层级，不靠纯字号差维持结构。
- 路径、locator id、技术标识使用 monospace。
- 密度调节优先改 spacing/token，不优先压缩字号。
