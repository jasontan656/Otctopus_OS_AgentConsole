---
doc_id: "ui.dev.docs.purpose_boundary"
doc_type: "topic_atom"
topic: "Purpose boundary for the showroom redevelopment"
anchors:
  - target: "00_UI_DEV_DOCS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This purpose doc belongs to the showroom docs index."
  - target: "../../frontend_dev_contracts/showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The generic showroom stack contract and the showroom-specific purpose must stay aligned."
  - target: "domains/00_GOVERNANCE_DOMAIN_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The workbench purpose must hand readers into domain-aware rendering docs."
  - target: "navigation/00_NAVIGATION_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Navigation is one concrete expression of the showroom purpose."
  - target: "canvas/00_CANVAS_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Canvas workspace is the other concrete expression of the showroom purpose."
---

# Showroom Purpose Boundary

## 当前用途
- 这个 showroom 现在的真实目标已经收敛为统一治理工作台，而不只是单一 skill 的演示页。
- 它必须在一个 coherent SPA shell 中同时承载：
  - 受治理文档包与其结构关系图
  - code graph 仓库与其关系可视面
  - AI 协作入口与上下文定位
  - 当前 workbench 自身的开发与重建文档
- 它不允许停留在对旧实现事故的静态三栏复刻上。

## 必须展示的内容类型
- A menu-first navigation surface for opening showroom panels.
- A canvas workspace that can host, focus, and close panels.
- Domain-aware panels for document graph, document packages, document reading, code graph, repo/library discovery, AI collaboration, runtime intent, and showroom overview.
- A clear boundary between generic frontend contracts, showroom-specific development docs, and runtime data sources.
- Inline navigation that lets the user jump between graph nodes, documents, repos, and AI context handles without manual path hunting.

## 非目标
- It is not a marketing landing page.
- It is not a fixed dashboard made of permanent columns.
- It is not a place to keep legacy UI code just because it still runs.
- It is not a UI that hardcodes every document pack or repo as a bespoke page.
