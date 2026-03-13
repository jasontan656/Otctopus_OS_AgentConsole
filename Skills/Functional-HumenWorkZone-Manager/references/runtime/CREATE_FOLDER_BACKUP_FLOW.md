---
doc_id: functional_humenworkzone_manager.runtime.create_folder_backup_flow
doc_type: topic_atom
topic: Flow for backing up a folder into Backup_Management
anchors:
- target: BACKUP_MANAGEMENT_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Backup execution is one operational branch of the managed zone.
- target: BACKUP_NAMING_RULE.md
  relation: requires
  direction: downstream
  reason: Every backup needs a governed local name.
- target: BACKUP_README_MAINTENANCE_FLOW.md
  relation: triggers
  direction: downstream
  reason: Creating a backup must be followed by inventory maintenance.
---

# Create Folder Backup Flow

## 触发条件
- 当用户直接说“把某个文件夹备份”时，使用本流程。

## 固定步骤
1. 先确认待备份对象是一个目录。
2. 目标落位目录固定在 `/home/jasontan656/AI_Projects/Human_Work_Zone/Backup_Management/` 下。
3. 备份目录名必须先套用 `BACKUP_NAMING_RULE.md`。
4. 以“完整复制”的方式生成备份，不删减内部内容，不重组内部结构。
5. 复制完成后，立即更新 `Backup_Management/README.md`。
6. 在 `README.md` 里补一句说明这个备份是什么。

## 最小落地要求
- 不能把备份散放在 `Human_Work_Zone` 其他位置。
- 不能只复制目录而不补清单。
- 若同一来源多次备份，允许存在多个不同日期版本，但每个版本都必须独立登记。
