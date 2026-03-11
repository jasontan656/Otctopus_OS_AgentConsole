---
doc_id: "ui.dev.rules.identifier_lint"
doc_type: "tooling_usage"
topic: "Lint workflow for layer, container, and component identifiers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This lint workflow belongs to the frontend rules branch."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "The runnable showroom must stay in sync with the identifier lint."
  - target: "../layers/30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The lint workflow enforces the locator and identifier protocol."
---

# UI Identifier Lint Workflow

## Lint 负责的检查
- layer id 是否属于固定 catalog。
- 容器 id 是否符合 `layerId-containerName`。
- 组件 id 是否符合 `layerId-containerName-componentName`。
- 两字母短码是否全局唯一。
- registry 中声明的文件是否存在。
- 容器 / 组件文件是否正确绑定自身 id。

## 必用命令
- `npm run cli -- ui-identity-contract --json`
- `npm run cli -- lint-ui-identity --json`

## 使用时机
- 新增 layer、container、component 前先读 contract。
- 修改 `ui-dev/client/src/containers/*` 或 `ui-dev/client/src/components/*` 后必须重跑 lint。
