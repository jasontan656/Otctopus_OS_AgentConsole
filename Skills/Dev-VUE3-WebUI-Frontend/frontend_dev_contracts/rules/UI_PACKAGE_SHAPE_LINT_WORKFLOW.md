---
doc_id: "ui.dev.rules.package_shape_lint"
doc_type: "tooling_usage"
topic: "Lint workflow for reusable component package shape and export discipline"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This lint workflow belongs to the frontend rules branch."
  - target: "../component_system/packaging/10_COMPONENT_PACKAGE_SHAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The lint workflow enforces the reusable component package-shape contract."
  - target: "../code_architecture/packages/30_COMPONENT_EXPORT_GUIDE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The lint workflow also checks export discipline."
  - target: "../code_architecture/packages/40_COMPONENT_REGISTRY_GUIDE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The lint workflow also checks registry discipline."
---

# UI Package Shape Lint Workflow

## Lint 负责的检查
- component 是否拥有独立 package 目录。
- package 内是否存在 `ComponentName.vue`、`ComponentName.contract.ts`、`ComponentName.tokens.css`、`index.ts`。
- `index.ts` 是否导入局部样式并导出默认组件与 contract。
- registry 中声明的 package 路径是否与文件系统一致。

## 必用命令
- `npm run cli -- ui-package-contract --json`
- `npm run cli -- lint-ui-package-shape --json`

## 使用时机
- 新增或迁移组件 package 后立即运行。
- 修改 `ui-dev/client/src/components/` 结构后必须运行。
