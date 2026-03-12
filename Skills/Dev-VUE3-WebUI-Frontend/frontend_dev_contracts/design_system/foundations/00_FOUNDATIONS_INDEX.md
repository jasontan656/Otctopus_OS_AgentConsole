---
doc_id: "ui.dev.design_system.foundations.index"
doc_type: "ui_dev_index"
topic: "Index of foundational design-system contracts"
node_role: "routing_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_DESIGN_SYSTEM_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This routing index belongs to the design-system branch."
  - target: "10_DESIGN_TOKEN_MODEL.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The token model is the primary foundation document."
  - target: "20_SEMANTIC_STYLE_MAPPING.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Semantic style mapping translates raw tokens into reusable UI surfaces."
---

# Foundations Index

## 本层负责
- token catalog
- semantic style 语义映射
- 全局样式与局部组件 package 的共享变量接口

## 读取顺序
1. `10_DESIGN_TOKEN_MODEL.md`
2. `20_SEMANTIC_STYLE_MAPPING.md`
