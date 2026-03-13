---
doc_id: functional_humenworkzone_manager.runtime.organize_books_and_readings_flow
doc_type: topic_atom
topic: Flow for organizing the managed reading library
anchors:
- target: BOOKS_AND_READINGS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Organizing books and readings is one operational branch of the managed zone.
- target: BOOK_NAMING_RULE.md
  relation: requires
  direction: downstream
  reason: Each item needs a governed local name.
- target: BOOK_LIBRARY_README_MAINTENANCE_FLOW.md
  relation: triggers
  direction: downstream
  reason: Organizing items must be followed by library index maintenance.
---

# Reading Library Organization Flow

## 触发条件
- 当用户要整理书籍、阅读资料、学习笔记或阅读资料包时，使用本流程。

## 固定步骤
1. 先确认对象属于书籍、阅读物、学习资料或资料包，而不是开源 repo。
2. 目标落位目录固定在 `/home/jasontan656/AI_Projects/Human_Work_Zone/Books_and_Readings/` 下。
3. 条目名称必须先套用 `BOOK_NAMING_RULE.md`。
4. 迁移完成后，立即更新根 `README.md`。
5. 若条目是多文件资料包，必要时在包内补本地 `README.md`。

## 最小落地要求
- 不能只迁移不改成统一命名。
- 不能只重命名不补导航 README。
- 若资料包内有多个版本或语言，应让文件名能区分它们。
