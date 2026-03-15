---
doc_id: skillsmanager_mirror_to_codex.path.install_route.validation
doc_type: validation_doc
topic: Install route validation
---

# Install 路由校验

## 当前动作完成条件
- `status=route_required`。
- `resolved_mode=install`。
- JSON 中包含 `next_skills` 与 `next_steps`。
- codex 根不会因为当前命令产生新技能目录。
