---
doc_id: dev_octopusos_constitution_projectstructure.governance.doc_structure_policy
doc_type: topic_atom
topic: Doc-structure policy for the OctopusOS project-structure constitution skill
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends maintenance and governance reads here.
- target: SKILL_EXECUTION_RULES.md
  relation: pairs_with
  direction: lateral
  reason: Structure policy and execution rules are the two core governance atoms of this skill.
---

# Skill Doc-Structure Policy

## 强制声明
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须显式应用的规则。
- 若当前结构与 facade / routing / topic atom 原则冲突，优先整体重建结构，而不是局部补丁。

## 必做项
- 以 `SKILL.md` 入口为 tree root，向下至少补齐一层 routing doc。
- 与章鱼OS项目级结构直接相关的深规则，应下沉到 `references/project_structure/` 的单 topic 原子文档，不回流到门面。
- 所有 markdown 文档都应保留可被 anchor graph 消费的 frontmatter 与 anchors。

## 当前结构边界
- 当前 skill 采用 `facade -> task routing -> governance atoms + project_structure atoms` 的 basic 结构。
- `references/project_structure/` 只容纳项目级对象、模块、bundle、容器与文件夹结构规则；域内实现规范不得混入这里。
- 当前未声明 runtime contract，也未声明专属 CLI；因此 `references/tooling/` 只承担“当前无工具现状”和未来扩展约束，不承担运行规则。
