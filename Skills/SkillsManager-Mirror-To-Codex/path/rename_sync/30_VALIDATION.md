---
doc_id: skillsmanager_mirror_to_codex.path.rename_sync.validation
doc_type: validation_doc
topic: Rename sync validation
---

# Rename 同步校验

## 当前动作完成条件
- `resolved_mode=rename`。
- JSON 中包含 `rename_from`、`staged_destination` 与最终 `destination`。
- 非 dry-run 时，codex 中不会保留旧名目录与新名目录并存。
- 若发生预先存在的新名目录冲突，结果中能体现清理与改名状态。
