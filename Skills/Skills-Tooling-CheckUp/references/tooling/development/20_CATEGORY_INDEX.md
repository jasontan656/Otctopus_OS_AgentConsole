---
doc_id: "skills_tooling_checkup.tooling.category_index"
doc_type: "topic_atom"
topic: "Category index for the local contract and directive modules"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The development entry routes readers into this category index."
  - target: "modules/MODULE_TEMPLATE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "If local modules evolve, this index must route readers into their module docs."
---

# Tooling Category Index

## 分类导航
- 架构与边界：`00_ARCHITECTURE_OVERVIEW.md`
- 模块清单：`10_MODULE_CATALOG.yaml`
- 合同模块：`modules/mod_contract.md`
- directive 模块：`modules/mod_directive.md`
- 运行时资产：`../../runtime_contracts/`
- 运行时与产物落点治理：`../../governance/OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md`
- 依赖基线：`../../governance/MANDATORY_TECHSTACK_BASELINE.md`
- 修正流程：`../../governance/TOOLING_REMEDIATION_PROTOCOL.md`
- 变更记录：`90_CHANGELOG.md`

## 分类维护规则
- 本技能当前有两个本地模块：`contract` 与 `directive`。
- 若新增本地工具，先更新模块目录，再补模块文档与对应 runtime contract 资产。
- 新 runtime-facing 合同类资产必须进入 `references/runtime_contracts/`，并保持 human/json 双文件一致。
