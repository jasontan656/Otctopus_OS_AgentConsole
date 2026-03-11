---
doc_id: "ui.dev.positioning.index"
doc_type: "index_doc"
topic: "Index of positioning and file-boundary contracts for the frontend development tree"
node_role: "index_doc"
domain_type: "frontend_contract_branch"
anchors:
  - target: "../00_UI_DEVELOPMENT_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This index is one branch under the frontend development contract entry."
  - target: "UI_TOOL_POSITIONING.md"
    relation: "indexes"
    direction: "downstream"
    reason: "Positioning is the primary document of this branch."
---

# Positioning Contracts

## 本分支负责
- `UI_TOOL_POSITIONING.md`
  - 定义 `frontend_dev_contracts/`、root resident docs、stage docs 与 `ui-dev/` 的职责边界。
- `UI_FILE_ORGANIZATION.md`
  - 定义哪些内容应该留在 `ui-dev/`，哪些内容应沉淀到合同树。

## 读取顺序
1. `UI_TOOL_POSITIONING.md`
2. `UI_FILE_ORGANIZATION.md`
