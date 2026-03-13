---
doc_id: "ui.dev.code_architecture.external_graph_dependency_governance"
doc_type: "ui_dev_guide"
topic: "Governance for external graph, render, and layout dependencies in frontend runtimes"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_TOPOLOGY_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "External graph dependency governance belongs to the topology branch."
  - target: "20_DEPENDENCY_DIRECTION_GUIDE.md"
    relation: "extends"
    direction: "cross"
    reason: "Third-party dependency rules refine the generic dependency direction guide."
  - target: "../packages/40_COMPONENT_REGISTRY_GUIDE.md"
    relation: "supports"
    direction: "cross"
    reason: "Graph wrappers and adapters still need stable identity and package registration."
---

# External Graph Dependency Governance

## 适用场景
- 面向 `document_graph`、workflow-like viewer、code graph、cluster explorer、dependency map 等 graph-heavy runtime。
- 目标是优先复用成熟外部依赖，而不是自研基础 graph engine / layout engine。

## 默认依赖轮廓
- `@vue-flow/core`：
  - 适用于 Vue 原生节点插槽、文档结构图、workflow-like 交互 surface。
  - 进入方式：只通过 `viewer adapter` / wrapper package 接入。
- `@vue-flow/background`、`@vue-flow/minimap`、`@vue-flow/controls`：
  - 适用于 `Vue Flow` surface 的底纹、视口控制和 minimap。
  - 进入方式：只作为 `Vue Flow` viewer shell 的配套包。
- `elkjs`：
  - 适用于 tree / layered / directional graph 的自动布局。
  - 进入方式：只通过 `layout adapter` 输出 positions / routing hints。
- `cytoscape`：
  - 适用于更大规模、可过滤、可探索的网络图与代码 graph。
  - 进入方式：只通过 `viewer adapter` 将产品 projection 映射为 elements。
- `cytoscape-elk`：
  - 只在 `Cytoscape.js` 的层次布局被验证需要时接入。
  - 不得作为所有 graph view 的默认前置依赖。

## 明确边界
- 第三方 graph 库不是产品事实源；产品事实源永远是 domain contract、projection shape、locator 与 registry。
- 不允许把外部库原生 schema 直接暴露给 panel container、业务 composable 或 acceptance witness。
- 更换 graph 引擎时，修改点必须收敛在 `viewer adapter` / `layout adapter` / wrapper package，而不是反向冲击业务组件树。
- `notation-specific` 工具，例如 `bpmn-js`，只有在真实 notation requirement 出现时才允许进入专用子域；禁止把它当通用 graph 底座。

## 包与身份治理
- 第三方 graph wrapper 也必须拥有稳定 package id / component id，并进入统一 registry。
- `GraphCanvas`、`GraphMinimap`、`GraphControls` 这类通用 wrapper 应作为 foundation 层组件，而不是散落到具体业务 panel。
- 若某图谱依赖只服务单一 panel，也必须先通过 adapter contract 定义输入/输出，再决定是否进入该 panel 局部包。
