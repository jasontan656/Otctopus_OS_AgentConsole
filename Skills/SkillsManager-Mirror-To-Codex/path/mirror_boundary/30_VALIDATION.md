---
doc_id: skillsmanager_mirror_to_codex.path.mirror_boundary.validation
doc_type: validation_doc
topic: Mirror boundary validation
---

# 镜像边界校验

## 当前动作完成条件
- 仅真正可同步的技能根进入结果。
- `.system` 只有在存在标记时才进入同步列表。
- codex 根禁留项会在 push 后清理。
- 产品级 `docs/`、`product_tools/` 等目录不会被镜像到 codex。
