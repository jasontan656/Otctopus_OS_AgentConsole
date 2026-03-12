---
doc_id: "ui.dev.code_architecture.copy_paste_reuse"
doc_type: "ui_dev_guide"
topic: "Copy-paste versus reuse guide for frontend components and local packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_CODE_GOVERNANCE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The copy-vs-reuse policy belongs to the governance branch."
  - target: "../../component_system/packaging/30_COMPONENT_REUSE_GUIDE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The packaging branch explains reuse at the component-composition level."
---

# Copy Paste Reuse Guide

## 优先级
- 优先复用已经被 contract 化的 package。
- 次选在同一容器域内建立新 package。
- 最后才是复制现有实现。

## 允许复制的条件
- 当前需求只是视觉近似，语义和交互已明显不同。
- 强行抽象会产生无意义 prop 泛化。

## 不允许复制的条件
- 只是换一个文案、颜色或轻微布局。
- 原组件已经具备稳定 API 和足够清晰的 style token。
