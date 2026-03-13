---
doc_id: "ui.tool.file_organization"
doc_type: "ui_dev_guide"
topic: "File organization rules for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_POSITIONING_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This guide belongs to the positioning branch."
  - target: "UI_TOOL_POSITIONING.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Positioning and file organization should be read together."
  - target: "../code_architecture/00_CODE_ARCHITECTURE_INDEX.md"
    relation: "refined_by"
    direction: "downstream"
    reason: "The code-architecture branch refines this coarse file boundary into an executable frontend topology."
  - target: "../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "supports"
    direction: "upstream"
    reason: "This guide constrains how product runtime code must be kept out of the skill."
---

# UI File Organization

## 必须留在产品代码仓的内容
- 页面与组件实现。
- SPA 容器实现。
- folder-first 组件 package。
- runtime bridge 与派生 view model。
- 容器 typed contract、layer registry 与共享前端协议类型。
- 全局 token、semantic、base、layout 资产。
- 与具体产品运行时绑定的服务端、适配层与实现级测试。

## 必须留在 `frontend_dev_contracts/` 的内容
- 前端开发合同索引。
- `layers/` 下的 layer catalog、locator 协议与命名 lint 工作流。
- `containers/` 下的容器角色、状态边界、布局权、交互协议和治理规则。
- `design_system/` 下的 token、semantic style、theme、typography 合同。
- `component_system/` 下的组件 black-box、API、package shape 与 style isolation 合同。
- `code_architecture/` 下的 folder topology、style asset placement、导出与复用策略。
- 组件、布局、运行链与复用边界规范。
- `rules/` 下的响应式与布局约束。

## 不应漂回 root 其他位置的内容
- 页面标题、布局细节、组件实验。
- viewer payload 组装和 service 脚本。
- `PreviewPayload` 一类 UI 语义类型。
