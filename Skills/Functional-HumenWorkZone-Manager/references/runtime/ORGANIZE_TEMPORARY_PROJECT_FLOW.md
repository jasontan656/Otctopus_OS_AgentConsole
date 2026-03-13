---
doc_id: functional_humenworkzone_manager.runtime.organize_temporary_project_flow
doc_type: topic_atom
topic: Intake flow for temporary projects
anchors:
- target: TEMPORARY_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: This flow operationalizes the temporary-project zone policy.
- target: TEMP_PROJECT_README_MAINTENANCE_FLOW.md
  relation: triggered_by
  direction: downstream
  reason: Every successful intake must update the temporary-project inventory.
- target: TEMP_PROJECT_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Intake may require a naming decision before relocation.
---

# Organize Temporary Project Flow

## 适用场景
- 用户要求“先收纳一下这个临时项目”。
- 某个项目当前散放在 `Human_Work_Zone` 之外，但应纳入后续可清理管理。

## 固定动作
1. 先确认目标目录属于“临时项目”，而不是开源项目、备份或书籍资料。
2. 先按 `TEMP_PROJECT_NAMING_RULE.md` 判断是否保留原名。
3. 目标落点固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Temporary_Projects/<project-folder>/`。
4. 默认执行整目录迁移，而不是复制残留双份。
5. 迁移完成后，同 turn 更新 `Temporary_Projects/README.md`。

## 写回要求
- 至少登记这些字段：
  - 项目名
  - 当前路径
  - 一句话基础作用
  - 项目本地 README 链接
  - 当前状态

## 默认状态
- 新迁入的临时项目默认状态写为 `active`。
- 若用户明确说明“已经停用，只是先留着”，可写成 `paused`。
