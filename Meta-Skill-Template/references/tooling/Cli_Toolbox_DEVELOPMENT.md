# Cli_Toolbox 开发文档（入口）

适用技能：`Meta-Skill-Template`

## 命名约束
- 本技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块文档模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- `Architecture`：系统级设计与边界定义。
- `Module Catalog`：模块清单、入口脚本、责任边界、状态。
- `Category`：按关注点组织（接口、运行态、测试、发布等）。
- `Module Docs`：每个模块独立文档，避免聚合为一个胖文件。
- `Changelog`：结构化记录开发文档体系的变更。

## 同步维护约束（强制）
- 工具变更时必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 对应模块文档（若影响模块行为）
- 禁止仅更新脚本而不更新开发文档索引/分类信息。
- 若模板契约变更影响“运行态规则如何被模型读取”，必须同步更新模板合同、架构手册与模板正文。
