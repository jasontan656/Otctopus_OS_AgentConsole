---
doc_id: "stages.motion_component_architecture"
doc_type: "stage_doc"
topic: "Motion language, reusable component boundaries, and code organization"
anchors:
  - target: "../../frontend_dev_contracts/layers/10_LAYER_TAXONOMY.md"
    relation: "details"
    direction: "downstream"
    reason: "The fixed layer catalog shapes how containers and components should be organized."
  - target: "../../frontend_dev_contracts/containers/model/10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "details"
    direction: "downstream"
    reason: "The container taxonomy defines the stable container roles that shape component architecture."
  - target: "../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "details"
    direction: "downstream"
    reason: "The runtime handoff stage expands the product-runtime implications."
  - target: "../../frontend_dev_contracts/component_system/00_COMPONENT_SYSTEM_INDEX.md"
    relation: "details"
    direction: "downstream"
    reason: "The component-system branch defines reusable black-box component packages and API rules."
  - target: "../../frontend_dev_contracts/code_architecture/00_CODE_ARCHITECTURE_INDEX.md"
    relation: "details"
    direction: "downstream"
    reason: "The code-architecture branch defines folder topology, style placement, and export discipline."
  - target: "../../frontend_dev_contracts/code_architecture/topology/30_EXTERNAL_GRAPH_DEPENDENCY_GOVERNANCE.md"
    relation: "details"
    direction: "downstream"
    reason: "Graph-heavy frontend products need explicit dependency and adapter boundaries."
  - target: "../../references/tooling/development/modules/mod_stage_contract_runtime.md"
    relation: "explained_by"
    direction: "downstream"
    reason: "The stage-contract runtime module explains how this architecture is surfaced in CLI contracts."
---

# Stage Motion Component Architecture

## 关注点
- 动效必须服务信息层级，不得抢夺 graph 阅读主线。
- 页面应逐步沉淀为可复用组件，而不是继续把所有逻辑堆在单文件里。
- 组件应以 folder-first package 落盘，自带 `.vue/.contract.ts/.tokens.css/index.ts`。
- 产品 runtime 的实现顺序必须固定为：先框架，再可复用底座，再独立组件；不允许跳过前两层直接堆具体组件。
- 每个独立组件都必须可追踪，拥有稳定 component id，并纳入统一 registry。
- 对 graph-heavy runtime，应先固定 `viewer adapter` / `layout adapter`，再接入外部库；不得让 `Vue Flow`、`Cytoscape.js` 或其他依赖直接变成业务组件的事实源。
- 代码组织需要反映：
  - layer catalog
  - app shell 与 route scene
  - 工作区容器层
  - panel 容器层
  - 数据装配层
  - 可复用组件层
  - 运行时接线层

## 目标
- 让前端合同稳定地驱动未来产品 UI 重构。
- 让 design system、component system、code architecture 三条合同都能直接反向驱动产品代码结构。
- 让每个小组件都能被独立追踪、复用、替换，而不是沦为一次性页面碎片。
- 让外部 graph/render/layout 依赖可替换、可审计，而不是在产品里散落成不可治理的插件调用。
