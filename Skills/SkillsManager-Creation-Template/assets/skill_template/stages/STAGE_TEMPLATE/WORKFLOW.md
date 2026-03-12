---
doc_id: "skill_creation_template.asset.stage_workflow_template"
doc_type: "template_doc"
topic: "Template for one stage workflow document"
anchors:
  - target: "INSTRUCTION.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Stage workflow should be read with stage instruction."
  - target: "../00_STAGE_INDEX_TEMPLATE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The stage index routes readers into stage workflow."
---

# <stage_name> Workflow Template

## 入口动作
- [进入阶段后必须先做的动作]

## 核心动作
- [当前阶段允许的核心执行动作]

## 回填与证据
- [当前阶段需要回填的文档、状态或机器产物]

## 退出门禁
- [阶段退出前必须满足的门禁]
