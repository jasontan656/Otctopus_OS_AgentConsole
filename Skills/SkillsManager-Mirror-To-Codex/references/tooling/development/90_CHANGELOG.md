# CHANGELOG

## 2026-03-12
- 新增显式 `Rename` 模式：`--mode rename --scope skill --skill-name <new> --rename-from <old>`。
- `Rename` 模式收敛为“新目录内容覆盖旧目录，再将 codex 目录名改为新名”，彻底消灭 rename 场景下的新旧双目录并存。
- 新增 CLI 回归测试，锁住 rename 参数校验与目录更名行为。

## 2026-03-11
- `scope=all` 的 Push 语义收敛为“只同步真正的技能根与 `.system/`”，不再把整个 repo 根目录直接镜像进 codex 安装目录。
- 为全量 Push 新增 `synced_entries` 与 `commands` 输出，显式暴露实际同步边界。
- 新增回归测试，锁住产品层目录不会污染 codex 安装目录。

## 2026-03-10
- `sync_mirror_to_codex` 新增 nested skill path 支持，并收敛 `skill_name` 为受控相对路径语义。
- 为 `.system/*` 增加 mirror 实际目录名到 codex 安装目录小写规范名的自动映射。
- 新增 CLI 回归测试，锁住 nested path、越界拒绝与 system skill 路由行为。

## 2026-02-28
- 收敛同步方向为单向 `mirror_to_codex`。
- 移除 `codex_to_mirror` 入口与相关文档。

## 2026-02-25
- 初始化 `Meta-Skill-Mirror`。
- 新增单入口 `scripts/Cli_Toolbox.py`。
- 定义双向同步能力（full/single）。
- 约束 mirror 根目录为可见路径 `Codex_Skills_Mirror`。

## 2026-03-11 naming
- canonical id 重命名为 `SkillsManager-Mirror-To-Codex`。
- 纳入 `SkillsManager-Naming-Manager` 的 `[SKILL-GOV]` registry。
