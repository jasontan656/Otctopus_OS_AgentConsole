---
doc_id: skill_creation_template.asset.toolbox_category_index_template
doc_type: template_doc
topic: Template for a generated skill's tooling category index
anchors:
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: implements
  direction: upstream
  reason: The category index template is routed from the development entry template.
- target: modules/MODULE_TEMPLATE.md
  relation: routes_to
  direction: downstream
  reason: The category index should route readers into module templates.
---

# Cli_Toolbox 开发文档分类索引

## 分类导航
- 架构与边界：`00_ARCHITECTURE_OVERVIEW.md`
- 模块清单与映射：`10_MODULE_CATALOG.yaml`
- 路由与治理：按需补充 `references/routing/` 与 `references/governance/`
- 复杂技能 profile：按需补充 `references/stages/` 与 `assets/templates/stages/`
- 模块文档：`modules/`
- 变更记录：`90_CHANGELOG.md`

## 分类维护规则
- 新增工具时，先更新模块目录，再补模块文档。
- 若分类结构变更，必须同步更新入口文档索引。
