---
doc_id: "skill_creation_template.asset.execution_rules_template"
doc_type: "template_doc"
topic: "Template for a generated skill's execution rules document"
anchors:
  - target: "SKILL_DOCSTRUCTURE_POLICY_TEMPLATE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Execution rules and doc-structure policy should stay aligned."
  - target: "../routing/TASK_ROUTING_TEMPLATE.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing should send readers here for deep execution rules."
---

# Skill Execution Rules Template

## 本地目的
- [写清本技能在当前原子文档中真正承载的执行规则]

## 当前边界
- [只写当前 topic 的规则，不重开新的大分叉]

## 局部规则
- [规则 1]
- [规则 2]
- [规则 3]

## 例外与门禁
- [当前 topic 的局部例外]
- [当前 topic 的进入或退出门禁]
