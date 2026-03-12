---
doc_id: "ui.dev.component_system.api_guide"
doc_type: "ui_dev_guide"
topic: "Component API guide for reusable component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_MODEL_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "API contracts belong to the component model branch."
  - target: "../packaging/10_COMPONENT_PACKAGE_SHAPE.md"
    relation: "supports"
    direction: "cross"
    reason: "Package shape must expose stable APIs and contracts."
---

# Component API Guide

## API 组成
- `props`
  - 明确输入数据，不以任意 `options` 对象兜底。
- `emits`
  - 明确上抛的交互意图，不直接改父层状态。
- `slots`
  - 仅在组件确实需要结构注入时提供。
- `expose`
  - 默认不暴露，确有 imperative 需求再单独声明。

## 反模式
- 用布尔爆炸代替清晰 variant。
- 为了一个页面临时需要而加入难以复用的业务 prop。
