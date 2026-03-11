---
doc_id: "ui.dev.container.layout.index"
doc_type: "ui_dev_index"
topic: "Index of layout authority contracts for SPA containers"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../00_CONTAINERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is the layout branch of the containers contract tree."
  - target: "10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The layout authority contract defines shell and workspace responsibility."
---

# Layout Authority Index

## 负责内容
- `10_APP_SHELL_AND_WORKSPACE_LAYOUT_AUTHORITY.md`
  - 定义 hero、runtime 状态栏、工作区三栏布局，以及在窄屏下如何重排。

## 权限边界字段
- 本分支涉及布局裁决权时，沿用统一字段：
  - `action`
  - `actor_id`
  - `scope`
  - `authz_result`
  - `deny_code`
  - `policy_version`
