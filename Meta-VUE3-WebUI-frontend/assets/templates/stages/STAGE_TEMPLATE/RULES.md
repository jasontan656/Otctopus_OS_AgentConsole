---
doc_id: "templates.stage_rules"
doc_type: "template_doc"
topic: "Rules template for one staged frontend node"
anchors:
  - target: "../README_STAGE_SYSTEM.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This rules template belongs to the stage system template cluster."
  - target: "../../../../references/runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "conforms_to"
    direction: "upstream"
    reason: "Stage rules templates must conform to the runtime contract."
---

# Stage Rules Template

## 内容要求
- 规则只约束当前 stage。
- 不能把 resident docs 规则和局部 stage 规则混写。
