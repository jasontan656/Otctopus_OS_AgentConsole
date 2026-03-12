---
doc_id: "ui.dev.component_system.test_surface"
doc_type: "ui_dev_guide"
topic: "Testing surface for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_GOVERNANCE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Testing rules belong to the component governance branch."
---

# Component Test Surface

## 组件最小质量面
- 可被单元测试或容器测试稳定挂载。
- 交互路径可通过稳定文案、事件或状态断言验证。
- locator 可帮助人类定位，但不能代替测试断言本身。
