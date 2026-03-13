---
doc_id: functional_humenworkzone_manager.runtime.open_source_project_readme_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for the open-source project inventory README
anchors:
- target: OPEN_SOURCE_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The inventory README is a required asset of the managed zone.
- target: PULL_OPEN_SOURCE_PROJECT_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: New repo intake must lead to an inventory update.
- target: OPEN_SOURCE_PROJECT_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Inventory entries should match the governed local folder name.
---

# Open Source Project README Maintenance Flow

## 维护对象
- 维护文件固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Open_Source_Projects/README.md`。

## 每次更新至少同步这些字段
- 项目名
- 当前本地路径或受管目录名
- 基础作用的一句话说明
- 指向项目本体 `README.md` 的内联链接
- 当前状态，例如：`legacy待迁入`、`已在集中区`、`归档观察`

## 更新原则
- 说明文字保持简短，可帮助用户回忆“这个项目是做什么的”即可。
- 链接优先指向项目本地副本里的 `README.md`，不强依赖外网地址。
- 若项目目录名调整了，inventory 必须同 turn 更新。
- 若项目不再保留，应在 inventory 中移除或改成归档状态，不要留下失真条目。
