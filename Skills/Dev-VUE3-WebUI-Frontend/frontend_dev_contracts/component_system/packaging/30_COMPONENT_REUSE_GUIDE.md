---
doc_id: "ui.dev.component_system.reuse_guide"
doc_type: "ui_dev_guide"
topic: "Reuse guide for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_PACKAGING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Reuse policy belongs to the packaging branch."
  - target: "../../code_architecture/governance/10_COPY_PASTE_REUSE_GUIDE.md"
    relation: "supports"
    direction: "cross"
    reason: "The governance branch explains when copy/paste is acceptable."
---

# Component Reuse Guide

## 何时复制
- 视觉结构近似但语义、交互、状态面已明显分叉时允许复制。
- 复制后必须改名并拥有自己的 contract，不允许“几乎相同但偷偷改 prop”。

## 何时复用
- 原组件已具备稳定 API 和稳定 variant。
- 新需求只是文案、轻微颜色或布局变化。
