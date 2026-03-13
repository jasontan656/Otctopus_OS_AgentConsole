---
doc_id: "dev_telegram_constitution.tooling.toolbox_development"
doc_type: "topic_atom"
topic: "Tooling development entry for the Telegram interface constitution skill"
anchors:
  - target: "Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development docs are paired."
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The development entry should route readers into the architecture overview."
---

# Cli_Toolbox 开发文档（入口）

适用技能：`Dev-Telegram-Constitution`

## 当前状态
- 当前无真实 CLI。
- 当前工具面为空，skill 只维护静态治理文档。

## 内联索引
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- 入口文档只做导航与约束，不承载未来所有工具实现细节。
- 模块目录记录“当前无工具”这一状态。
- 若未来新增工具，再引入具体模块文档。

## 同步维护约束（强制）
- 工具变更必须同步更新：
  - `Cli_Toolbox_USAGE.md`
  - `10_MODULE_CATALOG.yaml`
  - `20_CATEGORY_INDEX.md`
- 若未来新增工具模块，再补对应模块文档。
- 若工具会影响 facade / routing / atomic doc tree，必须同步更新 `references/routing/`、`references/governance/` 与 `references/telegram/`。

## 版本变更记录
- 2026-03-13 初始化：创建 `Dev-Telegram-Constitution` basic 技能骨架。
- 2026-03-13 收敛：当前 skill 仅提供静态 Telegram 治理文档，不提供 CLI。
