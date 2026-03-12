---
doc_id: "ui.dev.component_system.composition_guide"
doc_type: "ui_dev_guide"
topic: "Composition guide for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_PACKAGING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Composition rules belong to the packaging branch."
---

# Component Composition Guide

## 组合优先级
1. 先组合已有 component package。
2. 其次在同一容器内新增局部 package。
3. 只有在语义明显稳定后才提升为全局共享组件。

## 何时抽象
- 两个以上容器需要相同 role、相同 API、相同样式面时。
- 组件 locator、测试面、a11y 规则可以被同一套 contract 描述时。
