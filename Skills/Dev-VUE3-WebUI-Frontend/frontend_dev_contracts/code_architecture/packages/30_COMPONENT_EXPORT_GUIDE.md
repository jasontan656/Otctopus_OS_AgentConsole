---
doc_id: "ui.dev.code_architecture.export_guide"
doc_type: "ui_dev_guide"
topic: "Component export guide for ui-dev packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_PACKAGE_TEMPLATE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Export rules belong to the package template branch."
  - target: "../../rules/UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "enforced_by"
    direction: "downstream"
    reason: "Package export rules are enforced by the package-shape lint workflow."
---

# Component Export Guide

## 导出规则
- container 与其它共享组件一律从 `components/ComponentName` 目录入口导入。
- `index.ts` 必须执行：
  - 导入局部 `*.tokens.css`
  - 默认导出 `.vue`
  - 重导出 contract/type
