---
doc_id: functional_humenworkzone_manager.runtime.temporary_files_zone_policy
doc_type: topic_atom
topic: Dedicated temporary-file zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends temporary file governance tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The zone policy must obey the skill execution boundary.
- target: ORGANIZE_TEMPORARY_FILES_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Intake and creation are split into an operational flow.
---

# Temporary Files Zone Policy

## 目标目录
- 临时文件集中治理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Temporary_Files`。
- 该目录用于承载临时需要治理的 markdown 文件、临时证据文件、一次性整理稿，或其他尚未决定长期归宿的文件。

## 目录职责
- 本目录负责承载临时治理文件本体，以及后续清理前的索引导航。
- 根目录下必须长期维护 `README.md`，记录：
  - 当前有哪些临时治理文件或主题子目录
  - 每个条目的路径
  - 一句话用途说明
  - 当前状态，例如：`active`、`paused`、`ready_to_archive`

## 收纳原则
- 若任务对象是文件级临时治理材料，而不是完整项目目录，应优先进入本区，而不是混入 `Temporary_Projects`。
- 模型可根据当时意图决定：
  - 直接在本区创建单个文件
  - 先创建一个主题子目录，再在子目录中放置一组相关文件
- 默认不对文件内容做语义裁剪；重点是收纳、命名与后续可追溯性。

## 进入本区后的后续分流
- 若要把临时治理文件迁入本区，或在本区内创建新的临时治理文件，进入 `ORGANIZE_TEMPORARY_FILES_FLOW.md`。
