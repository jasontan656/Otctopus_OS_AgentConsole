---
doc_id: "ui.dev.component_system.accessibility_surface"
doc_type: "ui_dev_guide"
topic: "Accessibility surface for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_GOVERNANCE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Accessibility rules belong to the component governance branch."
  - target: "../../layers/30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Locator ids complement but do not replace accessibility surfaces."
---

# Component Accessibility Surface

## 规则
- button、input、search box 保持可聚焦与键盘触达。
- warning、status、selected state 需要不依赖颜色也能理解。
- graph 可视引擎至少保持点击、缩放、选中反馈可用。
- locator id 只能辅助协作，不替代正常按钮文本、标题层级和 placeholder。
