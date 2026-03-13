---
doc_id: functional_humenworkzone_manager.runtime.backup_naming_rule
doc_type: topic_atom
topic: Naming rule for local backup folders
anchors:
- target: BACKUP_MANAGEMENT_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Folder naming is a governed part of the backup zone.
- target: CREATE_FOLDER_BACKUP_FLOW.md
  relation: required_by
  direction: upstream
  reason: Backup execution needs a naming decision before copy.
- target: BACKUP_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Inventory entries should align with this naming rule.
---

# Backup Naming Rule

## 固定格式
- 本地备份目录名格式固定为：`<2个word>_bak_<日期>`。

## 命名解释
- `<2个word>` 使用 2 个英文词描述该备份源的最小识别语义。
- 两个词之间使用连字符连接，例如：`house-sale`、`agent-rules`、`skill-mirror`。
- `<日期>` 使用 `YYYY-MM-DD`。

## 例子
- `house-sale_bak_2026-03-13`
- `skill-mirror_bak_2026-03-13`
- `tax-docs_bak_2026-03-13`

## 禁止项
- 不要只写 `bak` 和日期而没有前缀语义。
- 不要使用 3 个以上的英文词。
- 不要用纯中文、无意义缩写或时间格式混写。
