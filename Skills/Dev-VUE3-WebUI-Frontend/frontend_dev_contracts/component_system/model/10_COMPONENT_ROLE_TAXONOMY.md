---
doc_id: "ui.dev.component_system.role_taxonomy"
doc_type: "ui_dev_guide"
topic: "Component role taxonomy for reusable Vue3 component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_MODEL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Role taxonomy belongs to the component model branch."
  - target: "../../containers/model/10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Component roles must not overlap or erase container roles."
---

# Component Role Taxonomy

## 组件角色
- primitive
  - 单一输入输出的小构件，例如搜索框、状态卡、chip。
- composite
  - 由多个 primitive 组合的中等构件，例如 detail hero、warning list。
- visual_engine
  - 承担复杂可视表达但不拥有全局业务状态，例如 graph canvas。
- dev_support
  - locator frame、legend、toolbar 这类开发支撑组件。

## 角色边界
- 组件不拥有 route 或 workspace 全局选择态。
- 组件不直接消费未经归一化的 runtime payload。
- visual_engine 可以有内部渲染状态，但不能越权为 scene/container 持有业务状态。
