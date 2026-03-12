---
doc_id: "ui.dev.component_system.style_isolation"
doc_type: "ui_dev_guide"
topic: "Style isolation rules for reusable Vue3 component packages"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_COMPONENT_GOVERNANCE_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Style isolation belongs to the component governance branch."
  - target: "../../design_system/foundations/10_DESIGN_TOKEN_MODEL.md"
    relation: "depends_on"
    direction: "upstream"
    reason: "Style isolation relies on the shared token model."
---

# Component Style Isolation

## 规则
- 组件局部样式默认放在组件 package 的 `*.tokens.css` 中。
- 组件 package 只能暴露局部 class 和局部变量，不允许重写 `body`, `:root`, `button`, `input` 等全局选择器。
- 页面级与容器级布局类应放在全局 `styles/` 体系，不放进组件 package。
- 若组件需要局部语义变量，应以 `--component-*` 别名形式映射到全局 token。

## 当前 showroom 的应用
- graph canvas、document item、anchor chip、runtime status card、locator 支撑组件都应拥有自己的局部样式文件。
- panel shell、dashboard grid、page hero、scene stack 这类容器/布局样式不应混入组件 package。
