---
doc_id: dev_telegram_constitution.tooling.toolbox_usage
doc_type: topic_atom
topic: Tooling usage entry for the Telegram interface constitution skill
anchors:
- target: Cli_Toolbox_DEVELOPMENT.md
  relation: pairs_with
  direction: lateral
  reason: Usage and development docs should stay aligned.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: governed_by
  direction: downstream
  reason: Tooling docs should respect doc-structure governance.
---

# Cli_Toolbox 使用文档

适用技能：`Dev-Telegram-Constitution`

## 当前状态
- 当前无专属 `Cli_Toolbox.py`。
- 当前 skill 只提供静态治理文档，不提供本地脚本、contract CLI 或生成器。
- 因此本技能的实际入口是：
  - `SKILL.md`
  - `references/routing/TASK_ROUTING.md`
  - `references/telegram/*.md`

## 同步维护要求
- 若未来新增工具，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若未来新增工具影响 skill 的读取路径，也必须同步更新：
  - `references/routing/TASK_ROUTING.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
  - 对应 `references/telegram/*.md`
