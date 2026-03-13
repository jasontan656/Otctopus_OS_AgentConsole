---
doc_id: functional_humenworkzone_manager.runtime.company_documents_readme_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for the company-document inventory README
anchors:
- target: COMPANY_DOCUMENTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The inventory README is a required asset of the company-document zone.
- target: ORGANIZE_COMPANY_DOCUMENTS_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: Intake must lead to an inventory update.
- target: COMPANY_FOLDER_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Inventory entries should align with the governed folder name.
---

# Company Documents README Maintenance Flow

## 维护对象
- 维护文件固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Company_Documents/README.md`。

## 每次更新至少同步这些字段
- 公司目录名
- 当前本地路径或受管目录名
- 基础作用的一句话说明
- 指向公司目录的本地链接
- 当前状态，例如：`active`、`paused`、`archive_candidate`

## 更新原则
- 说明文字保持简短，重点帮助用户快速回忆“这个公司目录主要装什么”。
- 目录名或状态调整后，清单必须同 turn 更新。
- 若某家公司后续确认不需要继续保留，应先把状态改成 `archive_candidate` 或直接移除，不要留下失真条目。
