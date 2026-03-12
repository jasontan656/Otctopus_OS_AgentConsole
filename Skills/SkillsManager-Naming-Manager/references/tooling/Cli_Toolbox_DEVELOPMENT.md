# Cli_Toolbox 开发文档（入口）

适用技能：`SkillsManager-Naming-Manager`

## 当前状态
- 当前没有本地 `Cli_Toolbox` 工具实现。
- 保留本目录是为了满足模板治理结构，并显式声明“无 CLI”这一事实。

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块文档模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只做导航与边界说明。
- 当 `modules: []` 时，表示当前技能没有任何本地 CLI 模块。
- 若未来出现 CLI，再补充具体模块文档。

## 同步维护约束（强制）
- 若未来新增 CLI，必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - `20_CATEGORY_INDEX.md`
  - 对应模块文档
- 若本技能继续保持无 CLI，禁止把模板占位文案重新写回这些文件。

## 版本变更记录
- `2026-03-11`：初始化 `SkillsManager-Naming-Manager` 的 tooling 文档骨架，并确认当前为“无本地 CLI”状态。
