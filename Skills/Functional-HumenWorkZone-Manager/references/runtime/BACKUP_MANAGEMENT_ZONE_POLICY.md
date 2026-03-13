---
doc_id: functional_humenworkzone_manager.runtime.backup_management_zone_policy
doc_type: topic_atom
topic: Dedicated backup management zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends backup tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The backup zone must obey the skill execution boundary.
- target: CREATE_FOLDER_BACKUP_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Executing a backup is a separate operational flow.
- target: BACKUP_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Backup inventory upkeep is split into its own maintenance flow.
- target: BACKUP_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Backup naming is a distinct rule set.
---

# Backup Management Zone Policy

## 目标目录
- 备份集中管理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Backup_Management`。
- 该目录是 `Human_Work_Zone` 下所有“人工要求长期留存的整目录备份”应当对齐的目标形态入口。

## 目录职责
- 本目录负责承载备份目录本体与长期维护的备份清单 `README.md`。
- `README.md` 必须记录：
  - 当前有哪些备份
  - 每个备份的简单描述
  - 备份源大致是什么对象

## 本区原则
- 备份动作默认只做完整复制，不做内容裁剪。
- 备份目录名必须遵守 `BACKUP_NAMING_RULE.md`。
- 只要新增、删除或替换备份，`README.md` 同 turn 更新。

## 进入本区后的后续分流
- 若要执行某个文件夹的备份，进入 `CREATE_FOLDER_BACKUP_FLOW.md`。
- 若要维护备份清单，进入 `BACKUP_README_MAINTENANCE_FLOW.md`。
- 若要决定备份目录名，进入 `BACKUP_NAMING_RULE.md`。
