---
doc_id: "skill_creation_template.asset.doc_structure_policy_template"
doc_type: "template_doc"
topic: "Template for a generated skill's doc-structure policy"
anchors:
  - target: "../routing/TASK_ROUTING_TEMPLATE.md"
    relation: "implements"
    direction: "upstream"
    reason: "Generated skills should reach doc-structure policy through routing."
  - target: "SKILL_EXECUTION_RULES_TEMPLATE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Doc-structure policy and execution rules are the two core governance atoms."
---

# Skill Doc-Structure Policy Template

## 强制声明
- `skill-doc-structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 facade / routing / topic atom 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- `SKILL.md` 只做 facade。
- 至少补齐一层 routing doc。
- 深规则下沉到单 topic 原子文档。
- 所有 markdown 文档补齐 `doc_structure` frontmatter 与 anchors。

## 双段式约定
- 若本技能属于模板或治理类 skill，可在原子文档中使用 `技能本体 / 规则说明` 双段式。
- 不得以双段式为理由让 facade 膨胀。
