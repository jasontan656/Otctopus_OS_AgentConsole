---
doc_id: skills_tooling_checkup.tooling.toolbox_development
doc_type: topic_atom
topic: Development entry for the skill-local CLI-first runtime surface
anchors:
- target: Cli_Toolbox_USAGE.md
  relation: pairs_with
  direction: lateral
  reason: Usage and development templates are paired.
- target: development/00_ARCHITECTURE_OVERVIEW.md
  relation: routes_to
  direction: downstream
  reason: The development entry should route readers into the architecture template.
---

# Cli_Toolbox 开发文档（入口）

适用技能：`SkillsManager-Tooling-CheckUp`

## 命名约束
- 本地工具入口固定为：`scripts/Cli_Toolbox.py`
- 本地工具别名固定为：
  - `Cli_Toolbox.contract`
  - `Cli_Toolbox.directive`
  - `Cli_Toolbox.govern_target`

## 内联索引（阅读顺序）
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块模板：`references/tooling/development/modules/MODULE_TEMPLATE.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只做导航与约束，不承载全部实现细节。
- 运行时指令源已经切换为 `references/runtime_contracts/*.json`。
- `*_human.md` 仅承载人类叙事 Part A 与镜像用 Part B，不再作为模型主运行时入口。
- legacy governance docs 仍可作为人类 authoring / audit reference，但不再是门面直接路由的主执行面。
- `govern-target` 是面向目标 skill 的 tooling surface 审计入口，负责输出目标感知的审计结果，而不是直接代替用户重写目标 skill。

## 同步维护约束（强制）
- 修改 `scripts/Cli_Toolbox.py` 后，必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - `20_CATEGORY_INDEX.md`
  - 对应模块文档
  - `references/runtime_contracts/`
- 新增任何面向模型运行时的 contract/workflow/instruction/guide 时，必须同时维护 `*_human.md + same-name .json`。

## 版本变更记录
- `2026-03-12` 初始化技能，起初声明无本地工具面。
- `2026-03-12` 新增运行时可观测性、结果落点、定向产物路径与历史迁移责任的治理轴线。
- `2026-03-12` 新增本地 `Cli_Toolbox.py`，把 runtime contract 与 directive 切换为 CLI-first JSON 输出。
