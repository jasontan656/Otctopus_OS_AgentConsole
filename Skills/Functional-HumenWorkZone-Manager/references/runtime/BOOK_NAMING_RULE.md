---
doc_id: functional_humenworkzone_manager.runtime.book_naming_rule
doc_type: topic_atom
topic: Naming rule for books and readings
anchors:
- target: BOOKS_AND_READINGS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Naming is a governed part of the books zone.
- target: ORGANIZE_BOOKS_AND_READINGS_FLOW.md
  relation: required_by
  direction: upstream
  reason: Organizing items needs a naming decision before writeback.
- target: BOOK_LIBRARY_README_MAINTENANCE_FLOW.md
  relation: referenced_by
  direction: upstream
  reason: Library index entries should align with this naming rule.
---

# Book Naming Rule

## 固定格式
- 单文件条目格式固定为：`<title-core>__<material-kind>.<ext>`。
- 多文件资料包格式固定为：`<title-core>__<material-kind>/`。

## 命名解释
- `<title-core>` 使用英文短语概括资料主标题或主题。
- `<material-kind>` 使用受控短语，例如：`book`、`reading-note`、`reading-index`、`web-article`、`prompt-manual`、`prompt-contract`、`reading-pack`。

## 目标形态
- 名字应让人一眼看出“这是什么资料”。
- 若同主题有不同语言或版本，应在文件名中继续写清差异。

## 禁止项
- 不要保留完全模糊的临时名。
- 不要把不同资料类型都混叫成同一种名字。
