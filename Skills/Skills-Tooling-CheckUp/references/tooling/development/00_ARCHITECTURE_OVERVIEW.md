---
doc_id: "skills_tooling_checkup.tooling.architecture_overview"
doc_type: "topic_atom"
topic: "Architecture overview for a skill that audits tooling code without adding a new toolbox"
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
- 用结构化文档约束“如何审查和修正别的 skill 的 tooling code”，同时明确本技能本身不再额外提供新的工具面。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 治理层：`references/governance/MANDATORY_TECHSTACK_BASELINE.md`、`references/governance/TOOLING_REMEDIATION_PROTOCOL.md`
3. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
4. 变更层：`90_CHANGELOG.md`

## 额外要求
- 本技能没有 machine-readable runtime contract，也没有本地 CLI 输出入口。
- 真正的执行层位于目标 skill 现有命令，而不是本技能自身。
- 若未来有人想给本技能新增工具，必须先证明目标 skill 现有工具链与 repo 基线无法承载该类审查/修正工作。
