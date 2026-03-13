---
doc_id: "ui.dev.code_architecture.dependency_direction"
doc_type: "ui_dev_guide"
topic: "Dependency direction guide for product frontend containers, components, composables, and contracts"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_TOPOLOGY_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Dependency direction belongs to the topology branch."
  - target: "../../containers/state/10_CONTAINER_STATE_OWNERSHIP.md"
    relation: "supports"
    direction: "cross"
    reason: "State ownership boundaries rely on clean dependency direction."
---

# Dependency Direction Guide

## 允许依赖
- container -> component / composable / contract / types
- component -> component(package) / contract / types
- composable -> contract / types
- styles -> token / semantic 层

## 禁止依赖
- component -> container
- component -> raw runtime server payload
- styles 局部 package -> 全局布局类文件
- composable -> Vue SFC

## 特殊说明
- `GraphCanvas` 作为 visual_engine，可以依赖自己的 contract 和类型，但不能反向依赖 panel container。
