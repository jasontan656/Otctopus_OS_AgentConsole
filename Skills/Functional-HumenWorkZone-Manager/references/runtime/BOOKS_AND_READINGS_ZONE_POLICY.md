---
doc_id: functional_humenworkzone_manager.runtime.books_and_readings_zone_policy
doc_type: topic_atom
topic: Dedicated reading library zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends books and readings tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The books zone must obey the skill execution boundary.
- target: ORGANIZE_BOOKS_AND_READINGS_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Organizing books and readings is a separate operational flow.
- target: BOOK_LIBRARY_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Library index upkeep is split into its own maintenance flow.
- target: BOOK_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Naming is a distinct rule set.
---

# Reading Library Zone Policy

## 目标目录
- 书籍与阅读物集中区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Books_and_Readings`。
- 该目录承接原先零散放在 `.Learning` 等位置的书籍、文章、学习笔记与阅读资料包。

## 目录职责
- 本目录负责统一命名、集中承载与长期维护导航 `README.md`。
- 根 `README.md` 必须记录当前有哪些书籍与阅读物。

## 目录形态
- 单文件条目可直接落在根层。
- 多文件资料包应使用目录承载；必要时在包内维护本地 `README.md`。

## 本区原则
- 书籍与阅读物的名字应做到“一眼可看出是什么资料”。
- 重命名只改变外层文件名或目录名，不改资料内容本体。
