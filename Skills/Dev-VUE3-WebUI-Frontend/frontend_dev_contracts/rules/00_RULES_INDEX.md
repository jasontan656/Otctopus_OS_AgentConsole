---
doc_id: "ui.dev.rules.index"
doc_type: "index_doc"
topic: "Index of layout and responsive frontend rule contracts"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This rule index is one branch under the frontend development contract entry."
  - target: "UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Layout adjustment is the first concrete rule in this branch."
  - target: "UI_IDENTIFIER_LINT_WORKFLOW.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Identifier lint is the enforcement rule for layer and node naming."
  - target: "UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Package-shape lint enforces the reusable component folder contract."
---

# Frontend Rules Index

## 本分支负责
- `UI_LAYOUT_ADJUSTMENT_RULES.md`
  - 定义展厅布局调整、信息层级和响应式切换约束。
- `UI_IDENTIFIER_LINT_WORKFLOW.md`
  - 定义 layer、container、component 标识的 lint 工作流。
- `UI_PACKAGE_SHAPE_LINT_WORKFLOW.md`
  - 定义组件 package 目录形状、局部样式、导出与 registry 一致性的 lint 工作流。

## 读取顺序
1. `UI_LAYOUT_ADJUSTMENT_RULES.md`
2. `UI_IDENTIFIER_LINT_WORKFLOW.md`
3. `UI_PACKAGE_SHAPE_LINT_WORKFLOW.md`
