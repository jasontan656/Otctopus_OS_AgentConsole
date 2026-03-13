---
doc_id: functional_humenworkzone_manager.runtime.book_library_readme_maintenance_flow
doc_type: topic_atom
topic: Maintenance flow for the books and readings library README
anchors:
- target: BOOKS_AND_READINGS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: The library README is a required asset of the managed zone.
- target: ORGANIZE_BOOKS_AND_READINGS_FLOW.md
  relation: triggered_by
  direction: upstream
  reason: Organizing items must lead to library index updates.
- target: BOOK_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Index entries should match the governed names.
---

# Book Library README Maintenance Flow

## 维护对象
- 维护文件固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Books_and_Readings/README.md`。

## 每次更新至少同步这些字段
- 条目名
- 类型
- 一句话描述
- 本地路径
- 当前状态

## 更新原则
- 根 README 负责让人快速知道有哪些书和阅读物。
- 若条目改名、迁移或归档，README 必须同 turn 更新。
- 多文件资料包建议在根 README 和包内 README 两边都可导航。
