---
doc_id: functional_humenworkzone_manager.governance.doc_structure_policy
doc_type: topic_atom
topic: Doc-structure policy for the Human_Work_Zone manager skill
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends governance reads here.
- target: SKILL_EXECUTION_RULES.md
  relation: pairs_with
  direction: lateral
  reason: Doc-structure policy and execution rules are the two core governance atoms.
---

# Skill Doc-Structure Policy

## 强制声明
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 facade / routing / topic atom 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- 以 `SKILL.md` 入口为 tree root，向下至少补齐一层 routing doc。
- 深规则继续下沉到单 topic 原子文档，不要重新堆回门面。
- 所有 markdown 文档补齐 `doc_structure` frontmatter 与 anchors。
