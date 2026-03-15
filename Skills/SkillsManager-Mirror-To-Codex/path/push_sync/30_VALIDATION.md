---
doc_id: skillsmanager_mirror_to_codex.path.push_sync.validation
doc_type: validation_doc
topic: Push sync validation
---

# Push 同步校验

## 当前动作完成条件
- `resolved_mode=push`。
- `scope=skill` 时，JSON 包含单一 `command`。
- `scope=all` 时，JSON 包含 `synced_entries`、`commands` 与 `removed_forbidden_entries`。
- `docs`、`product_tools` 这类非技能根不会进入同步列表。
