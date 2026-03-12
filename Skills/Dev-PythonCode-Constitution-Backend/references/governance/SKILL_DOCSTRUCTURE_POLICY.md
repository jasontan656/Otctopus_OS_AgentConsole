---
doc_id: "dev_pythoncode_constitution_backend.governance.doc_structure_policy"
doc_type: "topic_atom"
topic: "Doc-structure policy for the Python backend code constitution skill"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "The task routing doc sends skill-maintenance tasks here."
  - target: "SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Structure policy and execution rules are the two active governance atoms in this skill."
---

# Skill Doc-Structure Policy

## 强制声明
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 facade / routing / topic atom 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- 以 `SKILL.md` 入口为 tree root，向下至少补齐一层 routing doc。
- 与 Python 代码规范直接相关的深规则，应下沉到单 topic 原子文档，不回流到门面。
- 所有 markdown 文档都应保留可被 anchor graph 消费的 frontmatter 与 anchors。

## 当前结构边界
- 当前 skill 采用 `facade -> task routing -> governance atoms` 的 basic 结构。
- 当前未声明 runtime contract，也未声明专属 CLI；因此 `references/tooling/` 只承担“无工具现状”和未来扩展约束，不承担运行规则。
- 若未来新增具体 Python 规范条文，应优先新增原子文档，再由 routing doc 或 execution rules 把读者送入对应文档。
