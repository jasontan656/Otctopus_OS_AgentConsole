---
doc_id: "ui.dev.containers.index"
doc_type: "ui_dev_index"
topic: "Index of SPA container contracts for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The containers branch is a core branch of the frontend contract tree."
  - target: "model/00_CONTAINER_MODEL_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The model branch defines container roles and nesting."
  - target: "state/00_STATE_AND_DATA_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The state branch defines ownership and payload boundaries."
  - target: "layout/00_LAYOUT_AUTHORITY_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The layout branch defines shell, workspace, and panel authority."
  - target: "interaction/00_INTERACTION_PROTOCOL_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The interaction branch defines route, event, and overlay protocols."
  - target: "governance/00_CONTAINER_GOVERNANCE_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The governance branch defines permission, code placement, and test surfaces."
---

# Containers Contract Index

## 分支职责
- 本分支负责把未来产品运行时组织成清晰的 SPA 容器树，而不是继续让单文件页面承载全部职责。
- 容器合同治理的是：
  - 容器角色
  - 容器层级与嵌套
  - 状态所有权与 payload 归一化边界
  - 布局权与 slot 权
  - 路由、事件与运行时交互协议
  - 权限、代码落点、测试面

## 分支读序
- `model/00_CONTAINER_MODEL_INDEX.md`
  - 先确认有哪些容器，以及它们如何嵌套。
- `state/00_STATE_AND_DATA_INDEX.md`
  - 再确认状态和 payload 由谁拥有、谁只读。
- `layout/00_LAYOUT_AUTHORITY_INDEX.md`
  - 再确认壳层、工作区、面板的布局裁决权。
- `interaction/00_INTERACTION_PROTOCOL_INDEX.md`
  - 再确认 route、selection、overlay、live bridge 如何传递。
- `governance/00_CONTAINER_GOVERNANCE_INDEX.md`
  - 最后确认权限、目录落点、测试与可观测面。
