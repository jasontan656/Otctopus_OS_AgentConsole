---
doc_id: "templates.stage_instruction"
doc_type: "template_doc"
topic: "Instruction template for a single staged frontend workflow node"
anchors:
  - target: "../README_STAGE_SYSTEM.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This instruction template belongs to the stage system template cluster."
  - target: "../../../../references/stages/00_STAGE_INDEX.md"
    relation: "used_by"
    direction: "upstream"
    reason: "Instruction templates feed concrete staged skill stage definitions."
---

# Stage Instruction Template

## 适用场景
- 用于定义某一 stage 的目标与边界。
- 只表达该 stage 自身，不混入其他 stage 语义。
