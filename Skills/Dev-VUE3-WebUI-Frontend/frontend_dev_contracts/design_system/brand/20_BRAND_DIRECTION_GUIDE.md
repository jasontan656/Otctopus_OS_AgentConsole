---
doc_id: "ui.dev.design_system.brand_direction_guide"
doc_type: "ui_dev_guide"
topic: "Brand direction guide for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_BRAND_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Brand-direction rules belong to the brand branch."
  - target: "../../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "supports"
    direction: "cross"
    reason: "The product-runtime handoff stage should preserve a stable visual language that can be reused by product frontends."
---

# Brand Direction Guide

## 品牌方向
- 暖色 accent + 冷色 runtime/graph 辅助。
- 不走默认紫白模板，也不默认深色模式。
- 强调阅读优先、结构清晰、展厅感而非营销页堆叠。

## 扩展规则
- 若未来加入 dark theme，必须保留 semantic token 名不变，只替换 token 值。
- 主题切换不得要求组件 package 改 props 或复制样式。
