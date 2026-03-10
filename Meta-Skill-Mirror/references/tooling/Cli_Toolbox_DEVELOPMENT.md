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
- `Push` 模式负责实际 `rsync -a --delete`。
- `Install` 模式只返回外部技能链：
  - `Skill-creator`
  - `Skill-installer`
