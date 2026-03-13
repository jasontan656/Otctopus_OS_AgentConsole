---
doc_id: functional_humenworkzone_manager.runtime.temp_project_readme_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for the temporary-project inventory README
anchors:
- target: TEMPORARY_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The inventory README is a required asset of the temporary-project zone.
- target: ORGANIZE_TEMPORARY_PROJECT_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: Intake must lead to an inventory update.
- target: TEMP_PROJECT_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Inventory entries should align with the governed local folder name.
---

# Temporary Project README Maintenance Flow

## 维护对象
- 维护文件固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Temporary_Projects/README.md`。

## 每次更新至少同步这些字段
- 项目名
- 当前本地路径或受管目录名
- 基础作用的一句话说明
- 指向项目本体 `README.md` 的内联链接
- 当前状态，例如：`active`、`paused`、`ready_to_delete`

## 更新原则
- 说明文字保持简短，重点帮助用户快速回忆“这个临时项目是干什么的”。
- 链接优先指向项目本地副本里的 `README.md`。
- 若项目目录名调整了，清单必须同 turn 更新。
- 若项目确认不用了，应优先把状态改成 `ready_to_delete` 或直接移除，不要留下失真条目。
