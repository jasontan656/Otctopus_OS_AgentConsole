---
doc_id: "ui.dev.component_system.variant_guide"
doc_type: "ui_dev_guide"
topic: "Component variant guide for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_MODEL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Variant contracts belong to the component model branch."
  - target: "20_COMPONENT_API_GUIDE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Stable variant surfaces must be defined after the API surface is clear."
---

# Component Variant Guide

## 最小变体面
- 所有共享组件至少应考虑：
  - `default`
  - `active` 或 `selected`
  - `disabled`
  - `empty` 或 `no-data`
  - `loading` 或 `pending`

## 规则
- 若当前组件不需要其中某态，应在 contract 中说明由上层容器承担。
- 变体应使用稳定枚举、稳定类名或稳定 prop，不用布尔爆炸描述多个状态组合。
