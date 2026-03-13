---
doc_id: "ui.dev.code_architecture.component_folder_template"
doc_type: "ui_dev_guide"
topic: "Component folder template for product frontend reusable packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_PACKAGE_TEMPLATE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The folder template belongs to the package template branch."
  - target: "../../component_system/packaging/10_COMPONENT_PACKAGE_SHAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This template is the concrete implementation of the package-shape contract."
---

# Component Folder Template

## 模板
```text
components/ComponentName/
├── ComponentName.vue
├── ComponentName.contract.ts
├── ComponentName.tokens.css
└── index.ts
```

## 写法要求
- `ComponentName.vue`
  - 只保留组件实现。
- `ComponentName.contract.ts`
  - 导出 component role、variant、label、局部 palette 或辅助常量。
- `ComponentName.tokens.css`
  - 导出局部 class 与局部 `--component-*` 变量。
- `index.ts`
  - 导入 `*.tokens.css`，默认导出 `.vue`，并重导出 contract/type。
