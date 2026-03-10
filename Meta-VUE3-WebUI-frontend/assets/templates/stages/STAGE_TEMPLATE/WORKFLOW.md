---
doc_id: "templates.stage_workflow"
doc_type: "template_doc"
topic: "Workflow template for one staged frontend node"
anchors:
  - target: "../README_STAGE_SYSTEM.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow template belongs to the stage system template cluster."
  - target: "../../../../references/tooling/Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Workflow templates should align with CLI contract usage."
---

# Stage Workflow Template

## 内容要求
- 写清 entry actions。
- 写清 exit gates。
- 不把阶段切换规则写丢。
