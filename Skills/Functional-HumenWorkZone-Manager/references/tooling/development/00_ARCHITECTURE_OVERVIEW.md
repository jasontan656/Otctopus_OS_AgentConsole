---
doc_id: skill_creation_template.asset.toolbox_architecture_template
doc_type: template_doc
topic: Template for a generated skill's tooling architecture overview
anchors:
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: implements
  direction: upstream
  reason: The architecture template is routed from the development entry template.
- target: ../../governance/SKILL_EXECUTION_RULES.md
  relation: pairs_with
  direction: downstream
  reason: Tooling architecture should stay aligned with execution rules.
---

# Cli_Toolbox 开发文档架构总览

适用技能：`Functional-HumenWorkZone-Manager`

## 目标
- 用结构化文档支撑复杂 Toolbox，而不是依赖单一开发文档。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 额外要求
- 若技能存在运行态规则、约束、指引，开发架构必须明确 machine-readable 合同、CLI 输出入口与 markdown 审计版的关系。
- 若 skill 已采用 doc-structure 治理，开发架构必须说明 facade、routing 与原子文档如何分工。
- 若技能属于 staged CLI-first 复杂 profile，开发架构还必须明确 resident docs、阶段目录与阶段合同。
