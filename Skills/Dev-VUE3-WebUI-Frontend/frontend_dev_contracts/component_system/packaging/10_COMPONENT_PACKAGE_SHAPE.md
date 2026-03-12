---
doc_id: "ui.dev.component_system.package_shape"
doc_type: "ui_dev_guide"
topic: "Folder-first package shape for reusable Vue3 components"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_PACKAGING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Package shape belongs to the packaging branch."
  - target: "../../code_architecture/packages/10_COMPONENT_FOLDER_TEMPLATE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The architecture branch provides the concrete file-template mapping."
  - target: "../../rules/UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "enforced_by"
    direction: "downstream"
    reason: "Package shape is enforced through the package lint workflow."
---

# Component Package Shape

## 默认目录形状
```text
components/ComponentName/
├── ComponentName.vue
├── ComponentName.contract.ts
├── ComponentName.tokens.css
└── index.ts
```

## 可选文件
- `ComponentName.types.ts`
  - 当组件类型复杂且不适合放入 `contract.ts` 时使用。
- `README.md`
  - 当组件被多个容器或多个技能复用时使用。
- `__tests__/`
  - 当组件包含非平凡交互或渲染规则时使用。

## 强制规则
- 容器和其它组件只能从 package 目录入口 `index.ts` 导入共享组件。
- `index.ts` 必须导出默认组件，并暴露 contract 常量或类型。
- `*.tokens.css` 必须只声明组件局部变量与局部类名，不复制全局 reset。
