---
doc_id: "dev_telegram_constitution.tooling.architecture_overview"
doc_type: "topic_atom"
topic: "Tooling architecture overview for the Telegram interface constitution skill"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The architecture overview is routed from the development entry."
  - target: "../../governance/SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "Tooling architecture should stay aligned with execution rules."
---

# Cli_Toolbox 开发文档架构总览

适用技能：`Dev-Telegram-Constitution`

## 目标
- 明确本技能当前没有本地 CLI，同时保留未来增加工具时的文档落点。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 变更层：`90_CHANGELOG.md`

## 额外要求
- 本技能当前无 machine-readable runtime contract。
- 本技能当前规则入口是 `facade -> routing -> telegram atoms`。
- 若未来新增 Telegram checker 或 capability generator，必须先在 `references/tooling/` 落文档，再补脚本。
