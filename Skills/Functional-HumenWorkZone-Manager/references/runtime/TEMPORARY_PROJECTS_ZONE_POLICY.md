---
doc_id: functional_humenworkzone_manager.runtime.temporary_projects_zone_policy
doc_type: topic_atom
topic: Dedicated temporary-project zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends temporary project tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The zone policy must obey the skill execution boundary.
- target: ORGANIZE_TEMPORARY_PROJECT_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Intake and relocation are split into an operational flow.
- target: TEMP_PROJECT_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Inventory upkeep is managed as a separate maintenance flow.
- target: TEMP_PROJECT_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Naming decisions are governed separately.
---

# Temporary Projects Zone Policy

## 目标目录
- 临时项目集中管理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Temporary_Projects`。
- 该目录用于承载“一次性小项目、短期试验项目、暂不确定是否长期保留的项目目录”。

## 目录职责
- 本目录负责承载临时项目本体，以及后续清理前的清单导航。
- 本目录下必须长期维护 `README.md`，记录：
  - 当前有哪些临时项目
  - 每个项目的基础作用
  - 指向项目本体 `README.md` 的本地链接
  - 当前状态，例如：`active`、`paused`、`ready_to_delete`

## 收纳原则
- 只要某个目录被判定为“暂时保留、后面可能清理”的项目，就应进入本区，而不是继续留在 workspace 根层。
- 默认执行整目录迁移，不做内容裁剪，不改项目内部结构。
- 若用户已经给了一个明确可识别的项目目录名，首次迁入时允许保留该名字；若名字过于模糊，再进入命名规则分支决定是否重命名。

## 进入本区后的后续分流
- 若要把外部临时项目迁入本区，进入 `ORGANIZE_TEMPORARY_PROJECT_FLOW.md`。
- 若要维护项目清单或状态，进入 `TEMP_PROJECT_README_MAINTENANCE_FLOW.md`。
- 若要决定目录名或校验命名，进入 `TEMP_PROJECT_NAMING_RULE.md`。
