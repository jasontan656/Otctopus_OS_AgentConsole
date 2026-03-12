---
doc_id: "ui.dev.docs.domains.workbench_model"
doc_type: "topic_atom"
topic: "Unified governance workbench model for document and code graph domains"
anchors:
  - target: "00_GOVERNANCE_DOMAIN_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workbench model belongs to the domain branch."
  - target: "../panels/10_SHOWROOM_PANEL_CATALOG.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The workbench domain model constrains which panels the shell must provide."
  - target: "../../../frontend_dev_contracts/showroom_runtime/VIEWER_STACK_AND_REUSE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The generic showroom stack contract must stay aligned with the domain-aware workbench model."
---

# Unified Governance Workbench Model

## 核心定义
- 统一前端壳的目标不是把所有内容变成同一种图，而是用同一套 menu/canvas/panel 体系承载多个治理域。
- 每个治理域都必须显式暴露自己的：
  - domain id
  - source root
  - viewer projection
  - available panels
  - jump targets
- 当前至少支持两类治理域：
  - `document_graph`
  - `code_graph`

## 域边界
- `document_graph`
  - 面向受治理文档包、文档树、anchor graph、原文阅读与规则跳转。
- `code_graph`
  - 面向已建图 repo、模块/cluster 关系、symbol/file 引用、上下游影响与 AI 辅助检索。
- 两类治理域都可出现在同一个 workspace，但它们的关系语义、legend、过滤器和辅助说明必须独立显示。

## 统一壳约束
- 统一的是：
  - app shell
  - menu taxonomy
  - canvas lifecycle
  - panel docking behavior
  - locator / AI entry handoff
- 不统一的是：
  - 源事实 schema
  - 原生关系词
  - 域内 legend
  - 域内 query/filter 语义

## AI 入口定位
- AI 入口是工作台级能力，不属于单一 panel 私有按钮。
- AI 入口必须能消费当前焦点对象的 locator、domain id、source root 与 selection context。
- 从 graph 或 reader 发起 AI 协作时，只能发送当前投影层允许暴露的上下文句柄，不能让 UI 临时猜原始数据结构。
