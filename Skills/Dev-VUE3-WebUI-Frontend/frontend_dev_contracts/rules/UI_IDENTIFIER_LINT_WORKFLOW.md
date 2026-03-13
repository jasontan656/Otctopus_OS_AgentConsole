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
  - target: "../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "supports"
    direction: "upstream"
    reason: "The product-runtime handoff stage must stay in sync with the identifier lint."
  - target: "../layers/30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The lint workflow enforces the locator and identifier protocol."
---

# UI Identifier Lint Workflow

## 当前状态
- 当前技能不再存放产品 UI 代码，因此本 workflow 处于 future-only 阶段。
- 在新的 UI 代码根重新引入前，不应把本文件误读成“当前已有可执行 lint”。

## 未来恢复时负责的检查
- layer id 是否属于固定 catalog。
- 容器 id 是否符合 `layerId-containerName`。
- 组件 id 是否符合 `layerId-containerName-componentName`。
- 两字母短码是否全局唯一。
- registry 中声明的文件是否存在。
- 容器 / 组件文件是否正确绑定自身 id。

## 恢复条件
- 只有当新的 SPA menu + canvas UI 实现落到具体产品代码仓后，本 workflow 才能重新绑定真实 CLI。
- 在此之前，命名协议只作为开发文档与未来实现约束存在。
