---
doc_id: "templates.stage_index"
doc_type: "template_doc"
topic: "Template for a staged-skill stage index"
anchors:
  - target: "../../../references/stages/00_STAGE_INDEX.md"
    relation: "used_by"
    direction: "upstream"
    reason: "The live stage index is derived from this template shape."
  - target: "README_STAGE_SYSTEM.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "The stage index template belongs to the stage system template cluster."
---

# Stage Index Template

## 顶层常驻文档
- `<resident_doc>`

## 统一入口
- `stage-checklist`
- `stage-doc-contract`
- `stage-command-contract`
- `stage-graph-contract`

## 阶段集合
| stage_id | objective | checklist | doc_contract | command_contract | graph_contract | exit_signal |
|---|---|---|---|---|---|---|
| `<stage_id>` | `<objective>` | `stage-checklist` | `stage-doc-contract` | `stage-command-contract` | `stage-graph-contract` | `<exit_signal>` |
