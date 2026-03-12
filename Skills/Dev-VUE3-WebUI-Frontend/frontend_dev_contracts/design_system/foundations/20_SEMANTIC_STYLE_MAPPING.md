---
doc_id: "ui.dev.design_system.semantic_mapping"
doc_type: "ui_dev_guide"
topic: "Semantic style mapping from tokens to reusable UI surfaces"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_FOUNDATIONS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Semantic style mapping belongs to the foundations branch."
  - target: "10_DESIGN_TOKEN_MODEL.md"
    relation: "depends_on"
    direction: "upstream"
    reason: "Semantic styles are derived from the token model."
  - target: "../../code_architecture/packages/20_STYLE_ASSET_PLACEMENT.md"
    relation: "supports"
    direction: "cross"
    reason: "Style asset placement must separate global semantic styles from local package tokens."
---

# Semantic Style Mapping

## 必须存在的语义面
- `page-shell`
  - 顶层页面背景、整体留白、最大宽度与外层氛围。
- `hero-surface`
  - 顶部 hero、说明性框、路线图说明。
- `panel-surface`
  - 侧栏、graph、reader、runtime status 等主面板。
- `interactive-control`
  - button、input、chip、toggle。
- `status-surface`
  - warning、error、success、runtime health。
- `overlay-surface`
  - locator overlay、未来 modal/drawer/palette。
- `graph-node-surface`
  - 文档 graph 节点与 edge label。

## 映射规则
- 语义类名负责表达角色，不表达页面位置。
- 同一语义面可因组件 package 局部变量做轻微偏移，但不能绕开全局语义 token。
- 组件 package 内出现 `background`, `border`, `shadow`, `color` 时，应先映射到本组件别名变量，再映射到全局 semantic token。

## 反模式
- `orange-box`, `left-panel-card`, `hero-blue-text` 这类物理命名。
- 不同组件各自定义 `selectedColor`、`primaryText` 但不回连全局 token。
