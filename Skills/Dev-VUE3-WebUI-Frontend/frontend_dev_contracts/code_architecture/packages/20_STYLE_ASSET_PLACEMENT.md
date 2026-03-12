---
doc_id: "ui.dev.code_architecture.style_asset_placement"
doc_type: "ui_dev_guide"
topic: "Style asset placement rules for global tokens and local package styles"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_PACKAGE_TEMPLATE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Style asset placement belongs to the package template branch."
  - target: "../../design_system/foundations/20_SEMANTIC_STYLE_MAPPING.md"
    relation: "depends_on"
    direction: "upstream"
    reason: "Style placement follows the semantic style mapping."
---

# Style Asset Placement

## 全局样式
- `styles/tokens.css`
  - 全局 token。
- `styles/semantic.css`
  - semantic style alias。
- `styles/base.css`
  - reset、body、font、root。
- `styles/layout.css`
  - page shell、hero、panel、dashboard grid 等容器/布局样式。

## 局部样式
- 每个组件 package 自带 `ComponentName.tokens.css`。
- 不允许把组件局部类名继续堆入 `layout.css`。

## 目的
- 全局样式只管共享环境与容器布局。
- 组件 package 只管自身 black-box 外观。
