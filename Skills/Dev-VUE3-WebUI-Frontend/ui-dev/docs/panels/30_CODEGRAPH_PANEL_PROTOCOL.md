---
doc_id: "ui.dev.docs.panels.codegraph_protocol"
doc_type: "topic_atom"
topic: "Code graph panel protocol derived from GitNexus viewer capabilities and local workbench constraints"
anchors:
  - target: "00_PANEL_CATALOG_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This protocol belongs to the panel branch."
  - target: "../domains/20_DISCOVERY_AND_RENDERING_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Code graph panels consume the shared discovery protocol."
  - target: "10_SHOWROOM_PANEL_CATALOG.md"
    relation: "details"
    direction: "upstream"
    reason: "This document expands the code-graph-facing panel portion of the catalog."
---

# Code Graph Panel Protocol

## 继承来源
- 本协议提炼自 `Human_Work_Zone/GitNexus/gitnexus-web` 中已验证的前端能力，而不是要求把旧实现原样迁回。
- 当前确认需要继承的能力包括：
  - `GraphCanvas`
  - `BackendRepoSelector`
  - `CodeReferencesPanel`
  - `ProcessesPanel`
  - `QueryFAB`
  - graph focus / zoom / highlight / selection workflow

## 面板职责
- `Repo Library Panel`
  - 展示已建图 repo、可用 graph 资源和基础状态。
- `Code Graph Panel`
  - 展示 repo graph、cluster/module 入口、节点聚焦、graph-level legend 和过滤器。
- `Code Reference Panel`
  - 展示 symbol/file 细节、引用、上下游线索和 graph-selected metadata。
- `AI Workspace Panel`
  - 接收当前 repo、node、selection context，作为 code graph 的工作台级协作入口。

## 保留与改写边界
- 必须保留：
  - 图谱为主的关系探索
  - repo 选择与自动切换入口
  - graph 节点聚焦、引用查看、AI 入口联动
- 必须改写：
  - 旧 GitNexus 的页面骨架
  - 旧组件视觉风格
  - 与本地 menu/canvas/panel 架构冲突的固定布局

## 视觉与交互约束
- code graph 面板必须遵守本技能既有 layer、container、design system 合同。
- code graph 不得单独形成第二套 app shell。
- code graph 的交互复杂度可以高于文档域，但入口、关闭、聚焦、跳转都必须回收到统一 workspace 生命周期。
