---
doc_id: "ui.dev.docs.panels.document_graph_protocol"
doc_type: "topic_atom"
topic: "Document graph panel protocol for governed doc packages inside the workbench"
anchors:
  - target: "00_PANEL_CATALOG_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This protocol belongs to the panel branch."
  - target: "../domains/20_DISCOVERY_AND_RENDERING_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Document graph panels consume the shared discovery protocol."
  - target: "10_SHOWROOM_PANEL_CATALOG.md"
    relation: "details"
    direction: "upstream"
    reason: "This document expands the document-facing panel portion of the catalog."
---

# Document Graph Panel Protocol

## 面板职责
- `Document Graph Panel`
  - 负责渲染当前文档包的结构关系图或 anchor graph 投影。
- `Document Library Panel`
  - 负责列出文档包、分支索引、原子文档与可打开入口。
- `Document Reader Panel`
  - 负责显示正文、frontmatter 摘要、anchors、warning 与可跳转目标。

## 联动规则
- 图上点击节点时，应优先打开或聚焦 `Document Reader Panel`。
- 文档正文中的内联跳转，应能把目标节点回显到 `Document Graph Panel`。
- 文档包切换时，不应清空整个 workspace；只应刷新与当前文档域绑定的面板内容。

## 可见语义
- 面板必须明确显示：
  - 当前 domain id
  - 当前 doc pack / skill root
  - 节点类型 legend
  - 关系类型 legend
  - 发现状态或 contract warning
- 当关系未确认或目标缺失时，应以可读 warning 表达，而不是静默省略。
