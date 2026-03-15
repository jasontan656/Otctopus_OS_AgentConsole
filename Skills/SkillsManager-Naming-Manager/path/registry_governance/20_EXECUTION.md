---
doc_id: skillsmanager_naming_manager.path.registry_governance.execution
doc_type: topic_atom
topic: Registry governance execution
reading_chain:
- key: skill_registry
  target: 25_SKILL_REGISTRY.md
  hop: next
  reason: Registry snapshot follows the governance model.
---

# 注册治理实施

## 最少登记字段
- `canonical_id`
- `display_name`
- `prefix`
- `family`
- `role_tag`
- `status`
- `trigger_summary`

## registry 使用方式
- registry 是逻辑主表，不靠目录猜测 family 或 prefix。
- 当用户说“使用某 prefix 系列全技能”时，应以 registry 字段为准。
- 一个技能默认只应有一个主 prefix 和一个主 family，避免主路由歧义。

## 写入语义
- 注册动作默认按 `canonical_id` 执行 upsert。
- 已存在同一 `canonical_id` 时，应更新原条目的展示名、归类、状态与触发摘要。
- 只有 `canonical_id` 不存在时，才创建新登记。

## 下一跳列表
- [skill_registry]：`25_SKILL_REGISTRY.md`
