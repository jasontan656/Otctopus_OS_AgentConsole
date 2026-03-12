---
doc_id: "ui.dev.design_system.token_model"
doc_type: "ui_dev_guide"
topic: "Design token model for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_FOUNDATIONS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The token model belongs to the foundations branch."
  - target: "20_SEMANTIC_STYLE_MAPPING.md"
    relation: "precedes"
    direction: "downstream"
    reason: "Semantic style mapping depends on the token catalog."
  - target: "../../component_system/governance/10_COMPONENT_STYLE_ISOLATION.md"
    relation: "supports"
    direction: "cross"
    reason: "Component style isolation consumes the token model instead of hard-coded values."
---

# Design Token Model

## Token 轴线
- color
  - `--color-bg-*` 页面背景与 surface 背景。
  - `--color-fg-*` 正文、标题、muted 文本。
  - `--color-accent-*` 强调态、焦点态、选中态。
  - `--color-status-*` success/warning/error/info。
- spacing
  - 统一使用 `4px` 基线倍数：`xs/sm/md/lg/xl/2xl/3xl`。
- radius
  - 至少分 `sm/md/lg/xl/pill`，不得在组件内直接写任意圆角。
- shadow
  - 至少分 `soft/medium/strong/overlay`。
- border
  - 至少分 `subtle/default/strong/focus`。
- typography
  - `display/title/body/meta/code` 五组。
- motion
  - `duration-fast/normal/slow` 与 `ease-standard/emphasized`。
- z-index
  - `base/panel/overlay/locator` 四档。

## 使用规则
- 任何全局布局、容器、组件样式都优先引用 token，不直接写死物理值。
- 局部组件 package 可以声明自身别名变量，但必须映射回全局 token。
- 同一种语义不允许出现多套 token 命名。

## showroom 当前落地目标
- 顶层页面、panel、locator、graph 节点使用同一套背景、边框、阴影、文本和 accent token。
- runtime status、warning、anchor、selected node 等状态色统一走 status/accent token。
