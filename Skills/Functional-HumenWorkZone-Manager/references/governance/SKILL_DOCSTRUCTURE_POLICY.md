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
- 只要 `Human_Work_Zone` 下出现稳定子域，就应为该子域建立独立 routing 或 topic atom。
- 对“开源项目落位”“目录命名”“inventory README 维护”这类长期动作，必须一事一文档，不允许混成一篇大规则。
- 对“备份目录承载”“备份执行动作”“备份命名”“备份 README 维护”同样必须一事一文档，不允许混进开源项目分支。
- 对“分析区承载”“问题分析流程”“报告结构”“分析索引维护”同样必须一事一文档，不允许只靠零散报告文件隐式约定。
- 对“书籍区承载”“书籍命名”“批量迁移整理”“书籍导航 README 维护”同样必须一事一文档，不允许只靠人工记忆。
