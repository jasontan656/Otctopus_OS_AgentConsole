---
doc_id: skillsmanager_mirror_to_codex.references_tooling_cli_toolbox_development
doc_type: topic_atom
topic: Cli_Toolbox 开发文档（入口）
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

# Cli_Toolbox 开发文档（入口）

## 命名约束
- 工具入口固定为：`scripts/Cli_Toolbox.py`
- 模块前缀统一为：`Cli_Toolbox.sync_*`

## 内联索引（阅读顺序）
1. `development/00_ARCHITECTURE_OVERVIEW.md`
2. `development/20_CATEGORY_INDEX.md`
3. `development/10_MODULE_CATALOG.yaml`
4. `development/modules/mod_sync_mirror.md`
5. `development/90_CHANGELOG.md`

## 文档分类规则
- 架构层：解释职责边界与数据流。
- 分类层：按动作类型聚合模块。
- 模块层：描述参数、输入输出、失败模式。

## 同步维护约束（强制）
- 修改 `scripts/Cli_Toolbox.py` 后，必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `Cli_Toolbox_DEVELOPMENT.md`
  - `development/10_MODULE_CATALOG.yaml`
  - `development/modules/mod_sync_mirror.md`
- 禁止出现未文档化子命令。

## 已接入模块
- `Cli_Toolbox.sync_mirror_to_codex`

## 当前模式模型
- 抽象层负责根目录归一化、目标存在性检查与模式路由。
- 抽象层同时负责 `skill_name` 归一化、nested path 越界防护，以及 `.system/*` 的 source/destination 规范映射。
- `Push` 模式负责实际 `rsync -a --delete --checksum`。
- 当 `scope=all` 时，Push 必须先发现 mirror 顶层真正的技能根，禁止把整个 repo 根目录直接镜像到 codex 安装目录。
- `Install` 模式只返回外部技能链：
  - `Skill-creator`
  - `Skill-installer`
- `Rename` 模式只处理“mirror 已完成更名”的同步收口：
  - 要求 `--mode rename --scope skill --rename-from <old_name>`
  - 先用新目录内容覆盖 codex 旧目录
  - 再把 codex 旧目录名收敛为新目录名，防止新旧双目录并存
