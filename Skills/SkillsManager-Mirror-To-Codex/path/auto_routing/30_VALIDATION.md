---
doc_id: skillsmanager_mirror_to_codex.path.auto_routing.validation
doc_type: validation_doc
topic: Auto routing validation
---

# 自动导航校验

## 当前动作完成条件
- `auto` 只返回 `push` 或 `install` 之一。
- `rename` 缺少 `--rename-from` 时直接报错，不得静默回退。
- `install` 与 `rename` 的 scope 约束被严格执行。
- JSON 结果包含 `resolved_mode`，并与目标目录存在性一致。
