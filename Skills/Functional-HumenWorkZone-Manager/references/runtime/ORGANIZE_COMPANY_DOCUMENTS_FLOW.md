---
doc_id: functional_humenworkzone_manager.runtime.organize_company_documents_flow
doc_type: topic_atom
topic: Intake flow for company-document folders
anchors:
- target: COMPANY_DOCUMENTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: This flow operationalizes the company-document zone policy.
- target: COMPANY_DOCUMENTS_README_MAINTENANCE_FLOW.md
  relation: triggered_by
  direction: downstream
  reason: Every successful intake must update the company inventory.
- target: COMPANY_FOLDER_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Intake may require a naming decision before relocation.
---

# Organize Company Documents Flow

## 适用场景
- 用户要求“把这些公司资料收纳起来”。
- 某些公司资料目录当前散落在 `GoogleDriveDump` 或 `Human_Work_Zone` 根层之外。

## 固定动作
1. 先确认目标目录属于“公司资料”，而不是开源项目、备份、书籍或临时项目。
2. 先按 `COMPANY_FOLDER_NAMING_RULE.md` 判断是否需要重命名。
3. 目标落点固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Company_Documents/<company-folder>/`。
4. 默认执行整目录迁移，而不是复制出双份残留。
5. 迁移完成后，同 turn 更新 `Company_Documents/README.md`。

## 写回要求
- 至少登记这些字段：
  - 公司目录名
  - 当前路径
  - 一句话基础作用
  - 当前状态

## 默认状态
- 新迁入的公司目录默认状态写为 `active`。
- 若用户明确说明“只是历史留档”，可写成 `archive_candidate`。
