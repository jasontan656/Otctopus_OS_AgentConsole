---
doc_id: "ui.dev.layers.locator_protocol"
doc_type: "ui_dev_guide"
topic: "Visible locator identifiers and toggle protocol for containers and components"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_LAYERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This protocol belongs to the layers branch."
  - target: "20_LAYER_NODE_MAPPING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Identifiers render the layer-node mapping visible to humans."
  - target: "../rules/UI_IDENTIFIER_LINT_WORKFLOW.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The lint workflow enforces the protocol defined here."
---

# Locator Identifier Protocol

## 可见协议
- 每个容器和每个组件都必须有：
  - 全 id
  - 两字母缩略码
  - layer 归属
  - container 归属
- 当 locator toggle 打开时，UI 必须显式显示这些标识，方便人类直接说：
  - `定位 [GP]`
  - `问题发生在 PN-GraphPanel`

## 显示协议
- 容器显示：
  - `[短码] 全 id`
- 组件显示：
  - `[短码] 全 id`
- 全局必须存在 locator toggle，负责一键打开或关闭整站标识层。
- 全局必须存在 legend，帮助人类从短码快速反查完整节点。

## 缩略码约束
- 缩略码固定两位大写英文字母。
- 缩略码在 layer、container、component 范围内必须全局唯一。
