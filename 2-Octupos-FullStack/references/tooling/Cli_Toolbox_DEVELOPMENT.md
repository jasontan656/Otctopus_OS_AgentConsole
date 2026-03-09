# Cli_Toolbox 开发文档（入口）

适用技能：`2-Octupos-FullStack`

## 命名约束
- 工具统一命名为 `Cli_Toolbox.<tool_name>`。

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块文档模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只做导航与约束，不承载全部实现细节。
- 模块目录记录 tool alias、入口、状态与文档映射。
- 分类索引负责跨模块视图。
- 具体实现细节写入 `modules/<module_id>.md`。

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - 对应模块文档
- 若模板或工具会影响模型如何读取运行态规则，必须同步更新模板合同、架构手册与正文模板。
- 若技能使用 staged CLI-first profile，必须同步维护阶段目录与 runtime contract。

## 版本变更记录
- [日期] [变更摘要]
- 2026-03-09 新增 `Cli_Toolbox.materialize_container_layout`，用于第一阶段创建工作目录与 `Mother_Doc` 同名目录结构。
- 2026-03-09 升级 `Cli_Toolbox.materialize_container_layout`，按容器族补齐 `README.md + common/` 抽象层骨架，并为 `Mother_Doc` 特例补齐 `Mother_Doc/Mother_Doc/00_INDEX.md`。
- 2026-03-09 新增 `Cli_Toolbox.mother_doc_stage`、`Cli_Toolbox.implementation_stage`、`Cli_Toolbox.evidence_stage`，用于显式区分三阶段作用域与 carry-forward 规则。
