---
doc_id: "skill_creation_template.index.doc_tree"
doc_type: "index_doc"
topic: "Document tree and domain index for the skill template governance pack"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The facade routes broad readers here when they need the domain map."
  - target: "../routing/TASK_ROUTING.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Task routing and this index complement each other."
  - target: "../governance/SKILL_AUTHORING_CONTRACT.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Governance docs are a primary domain in the tree."
---

# Doc Tree Index

## 文档域
- `references/runtime/`
  - 本技能自己的运行合同与审计版说明。
- `references/routing/`
  - 按任务意图和 profile 继续分流的 routing docs。
- `references/governance/`
  - authoring contract、architecture playbook、staged profile reference、doc-structure enforcement。
- `references/tooling/`
  - `Cli_Toolbox` 的使用文档、开发入口和模块级开发文档。
- `assets/skill_template/`
  - `basic` 与 `staged_cli_first` 模板资产，以及运行合同模板与 stage kit。
- `tests/`
  - 生成器回归与后续结构验证入口。

## 读取建议
- 只需要判断当前动作时，优先走 `references/routing/`。
- 只需要明确硬约束时，优先走 `references/runtime/` 与 `references/governance/`。
- 只需要修改脚本或模板时，再进入 `references/tooling/` 与 `assets/skill_template/`。
