---
doc_id: skillsmanager_mirror_to_codex.references_tooling_development_20_category_index
doc_type: index_doc
topic: 分类索引
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# 分类索引

## SYNC_SCOPE
- `all`: 全量同步 skills 根目录。
- `skill`: 单技能目录同步。

## MODE_ROUTING
- `auto`: 先检查目标是否已存在，再在 `push/install` 之间自动导航。
- `push`: 目标已存在时执行覆盖同步。
- `install`: 目标不存在时返回外部技能链路。

## SAFETY
- `skill-name` 字符白名单校验。
- 固定根目录下路径拼接，拒绝越界。
- 目标缺失时禁止把首次安装伪装成覆盖同步。
