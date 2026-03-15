---
doc_id: functional_humenworkzone_manager.runtime.organize_temporary_files_flow
doc_type: topic_atom
topic: Intake flow for temporary governance files
anchors:
- target: TEMPORARY_FILES_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: This flow operationalizes the temporary-file zone policy.
---

# Organize Temporary Files Flow

## 适用场景
- 用户要求收纳一份或一组临时 markdown 文件。
- 用户要求创建一份临时治理文件，并希望先放在受管区，后续再决定长期归宿。
- 用户要求收纳临时证据文件、整理稿或其他短期待处理文件。

## 固定动作
1. 先确认目标对象是文件级临时治理材料，而不是完整项目目录。
2. 先判断这次更适合：
   - 直接在 `Temporary_Files/` 下创建单个文件，还是
   - 先创建一个主题子目录，再在其下放置一组相关文件。
3. 文件或子目录名由模型根据当时意图决定，但必须保持可读且可追溯。
4. 目标落点固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Temporary_Files/` 及其子目录。
5. 收纳或创建完成后，同 turn 更新 `Temporary_Files/README.md`。

## 写回要求
- 至少登记这些字段：
  - 条目名
  - 当前路径
  - 一句话用途
  - 当前状态

## 默认状态
- 新创建或新迁入的临时治理文件默认状态写为 `active`。
- 若用户明确说明“只是暂放，后面再归档”，可写成 `paused`。
