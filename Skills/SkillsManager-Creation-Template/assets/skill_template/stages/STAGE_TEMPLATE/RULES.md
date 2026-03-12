---
doc_id: "skill_creation_template.asset.stage_rules_template"
doc_type: "template_doc"
topic: "Template for one stage rules document"
anchors:
  - target: "INSTRUCTION.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Stage rules should stay aligned with stage instruction."
  - target: "../00_STAGE_INDEX_TEMPLATE.md"
    relation: "implements"
    direction: "upstream"
    reason: "The stage index routes readers into stage rules."
---

# <stage_name> Rules Template

## resident docs
- [当前阶段共享的 resident docs]

## 读取边界
- [当前阶段允许读取的范围]

## 写入边界
- [当前阶段允许写入的范围]

## 丢弃规则
- [切换阶段时需要显式丢弃的 focus]
