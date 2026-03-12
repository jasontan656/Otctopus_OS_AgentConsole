---
doc_id: "skills_tooling_checkup.governance.doc_structure_policy"
doc_type: "topic_atom"
topic: "Doc-structure policy for the skills tooling checkup skill"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing must hand off readers into the doc-structure policy."
  - target: "SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Doc-structure policy and execution rules are the two core governance atoms."
---

# Skill Doc-Structure Policy

## 强制声明
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 facade / routing / topic atom 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- 以 `SKILL.md` 入口为 tree root，向下至少补齐一层 routing doc。
- “依赖基线”和“修正流程”必须维持为两个独立 topic atom，不允许重新糊回门面或 routing。
- “运行时可观测性 / 产物落点治理”必须维持为独立 topic atom，不允许把路径根约束、文档声明要求和迁移责任零散塞进门面。
- 所有 markdown 文档都必须补齐 `doc_structure` frontmatter 与 anchors。

## 双段式约定
- 本技能属于治理类 skill，可在局部 topic atom 中使用 `技能本体 / 规则说明` 双段式。
- 双段式内容应保持在当前语义局部，不回流到入口节点。
