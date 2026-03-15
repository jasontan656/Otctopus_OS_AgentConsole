---
doc_id: skill_creation_template.path.skill_entry
doc_type: path_doc
topic: Single path-first entry for SkillsManager-Creation-Template
anchors:
- target: ../SKILL.md
  relation: implements
  direction: upstream
  reason: The facade points only to this file.
- target: template_creation/00_TEMPLATE_CREATION_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: Template creation is a primary behavior branch.
- target: maintenance/00_MAINTENANCE_ENTRY.md
  relation: routes_to
  direction: downstream
  reason: Maintenance is a primary behavior branch.
---

# Skill Main Entry

## 这个入口是干什么的
- 这是 `SkillsManager-Creation-Template` 当前唯一的主入口。
- 本文只负责把读者送入当前真正需要的行为分支，不展开深规则正文。
- 当前 skill root 只允许保留：`SKILL.md / path / agents / scripts`。

## 下一跳列表
- [模板创建入口]：`template_creation/00_TEMPLATE_CREATION_ENTRY.md`
  - 当任务是创建新模板或选择 `skill_mode` 时进入。
- [维护入口]：`maintenance/00_MAINTENANCE_ENTRY.md`
  - 当任务是维护三条创建链路的模板注册位置时进入。
