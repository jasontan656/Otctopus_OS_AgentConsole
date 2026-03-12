---
doc_id: "ui.dev.docs.panels.index"
doc_type: "index_doc"
topic: "Index of showroom panel catalog docs"
anchors:
  - target: "../00_UI_DEV_DOCS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index belongs to the showroom docs tree."
  - target: "10_SHOWROOM_PANEL_CATALOG.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The panel catalog defines the required showroom panels."
  - target: "20_DOCUMENT_GRAPH_PANEL_PROTOCOL.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The document graph protocol defines how doc packages and doc readers cooperate."
  - target: "30_CODEGRAPH_PANEL_PROTOCOL.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The code graph protocol defines which GitNexus-derived behaviors must survive in the new workbench."
---

# Panel Catalog Index

## 本分支负责
- `10_SHOWROOM_PANEL_CATALOG.md`
  - 定义当前 showroom 必须有哪些 panel。
- `20_DOCUMENT_GRAPH_PANEL_PROTOCOL.md`
  - 定义文档 graph、文档包、文档阅读与内联跳转的 panel 协作。
- `30_CODEGRAPH_PANEL_PROTOCOL.md`
  - 定义代码 graph、repo 发现、代码引用与 AI 入口的 panel 协作。
