---
doc_id: "skills_tooling_checkup.tooling.architecture_overview"
doc_type: "topic_atom"
topic: "Architecture overview for the skill-local contract plus directive toolbox"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The development entry routes readers into this architecture overview."
  - target: "../../governance/SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "Tooling architecture should stay aligned with execution rules."
---

# Tooling Architecture Overview

适用技能：`Skills-Tooling-CheckUp`

## 目标
- 用本地 CLI-first 合同约束“如何审查和修正别的 skill 的 tooling code”。
- 审查轴线现已包含两部分：既定依赖栈下的重复造轮子修正，以及 runtime 日志 / result 产物 / 定向产物落点的语义治理。

## 分层结构
1. 入口层：`scripts/Cli_Toolbox.py`
2. 运行时资产层：`references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json` 与各 topic directive JSON
3. human mirror 层：`references/runtime_contracts/*_human.md`
4. reference 层：`references/governance/`、`references/routing/`、`references/tooling/`
5. 变更层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`、`90_CHANGELOG.md`

## 额外要求
- 本技能现在拥有 machine-readable runtime contract，并以 CLI JSON 作为主运行时源。
- 本技能现在也拥有目标技能形态治理入口：`govern-target`。
- 真正的目标 skill 行为验证仍位于目标 skill 现有命令，而不是本技能自身。
- 若未来新增新的 runtime-facing contract/workflow/instruction/guide，必须以 `*_human.md + same-name .json` 双文件形态进入 `references/runtime_contracts/`。
