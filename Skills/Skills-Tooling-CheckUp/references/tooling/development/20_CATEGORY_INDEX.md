---
doc_id: "skills_tooling_checkup.tooling.category_index"
doc_type: "topic_atom"
topic: "Category index for a skill that intentionally has no local tooling modules"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The development entry routes readers into this category index."
  - target: "modules/MODULE_TEMPLATE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "If local modules ever exist, this index must route readers into their module docs."
---

# Tooling Category Index

## 分类导航
- 架构与边界：`00_ARCHITECTURE_OVERVIEW.md`
- 模块清单：`10_MODULE_CATALOG.yaml`
- 运行时与产物落点治理：`../../governance/OBSERVABILITY_AND_OUTPUT_GOVERNANCE.md`
- 依赖基线：`../../governance/MANDATORY_TECHSTACK_BASELINE.md`
- 修正流程：`../../governance/TOOLING_REMEDIATION_PROTOCOL.md`
- 变更记录：`90_CHANGELOG.md`

## 分类维护规则
- 当前没有本地模块，`modules/` 仅保留模板占位。
- 若未来新增本地工具，先更新模块目录，再补模块文档。
- 若仍无本地工具，则不得虚构模块清单。
