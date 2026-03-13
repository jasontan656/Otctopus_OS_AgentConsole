---
doc_id: "ui.dev.rules.product_blueprint_numeric_gate"
doc_type: "ui_dev_guide"
topic: "Numeric integrity gate for product-owned frontend spatial blueprints"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_RULES_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This numeric gate belongs to the frontend rules branch."
  - target: "UI_PRODUCT_MOTHER_DOC_LINT_WORKFLOW.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Numeric blueprint checks are executed through the product mother doc lint workflow."
---

# UI Product Blueprint Numeric Gate

## 目标
- 让产品 `mother_doc` 中已经进入 spatial blueprint 的对象，具备真正可计算的数值合同。
- 在文档层直接阻断缺尺寸、越界、未声明重叠和缺派生状态，而不是把这类问题推迟到实现代码里。

## blocking 维度
- blueprint 缺少 `frame_width`、`frame_height`、`x`、`y`、`w`、`h`
- blueprint / viewport / node 缺少必备字段键；字段允许为空，但键本身不得缺失
- `local_coordinate_space` 未定义
- child node 超出 frame / viewport / parent bounds
- sibling rectangles 发生 overlap，但未显式声明 `allow_overlap: true`
- 已声明 `allow_overlap: true`，但缺少 `overlap_mode`、`collision_policy`，或 `overlap_targets` 与实际冲突对象不匹配
- 文档声明了 `focus / compact / overlay / responsive`，却没有对应的可计算尺寸变体

## 处理原则
- 当前需求里已经出现的布局对象，必须补齐到可计算。
- 未来尚未进入需求树的新功能，不要求提前凭空设计。
- 允许存在 overlap，但 overlap 必须被显式声明，而不是靠读者猜测。
- 冲突语义字段遵循“可为空但不可缺键”原则；这使文档和代码保持同构，代码由浏览器解释，文档由 lint 解释。
