# Cli_Toolbox 开发文档（入口）

适用技能：`2-Octupos-FullStack`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 内联索引
1. `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. `references/tooling/development/10_MODULE_CATALOG.yaml`
3. `references/tooling/development/20_CATEGORY_INDEX.md`
4. `references/tooling/development/90_CHANGELOG.md`
5. `references/tooling/development/modules/*.md`

## 同步维护约束
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - 对应模块文档
- 若模板或工具会影响模型如何读取运行态规则，必须同步更新阶段文档、mother_doc 规则与 runtime contract。
