---
doc_id: "templates.stage_system"
doc_type: "template_doc"
topic: "Template guidance for defining staged frontend skills with contract quartets"
anchors:
  - target: "../../../references/stages/00_STAGE_INDEX.md"
    relation: "used_by"
    direction: "upstream"
    reason: "The live stage index is one concrete use of this template guidance."
  - target: "../../../references/runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "conforms_to"
    direction: "upstream"
    reason: "Template guidance follows the staged runtime contract."
---

# Stage System Template

## 用途
- 为 `staged_cli_first` 前端技能定义 stage quartet：
  - checklist
  - doc contract
  - command contract
  - graph contract
- 保证多阶段技能不会把所有规范混成一个胖文档。
