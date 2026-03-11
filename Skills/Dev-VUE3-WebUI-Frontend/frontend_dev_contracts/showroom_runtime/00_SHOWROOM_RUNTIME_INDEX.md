---
doc_id: "ui.dev.showroom_runtime.index"
doc_type: "index_doc"
topic: "Index of showroom runtime, stack, and service workflow contracts"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is one branch under the frontend development contract entry."
  - target: "VIEWER_STACK_AND_REUSE.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Viewer stack and reuse is the primary architecture contract of this branch."
---

# Showroom Runtime Contracts

## 本分支负责
- `VIEWER_STACK_AND_REUSE.md`
  - 定义 viewer 技术栈、复用方向和展厅母板角色。
- `VIEWER_SERVICE_WORKFLOW.md`
  - 定义 dev/build/systemd 运行链和服务工作流。

## 读取顺序
1. `VIEWER_STACK_AND_REUSE.md`
2. `VIEWER_SERVICE_WORKFLOW.md`
