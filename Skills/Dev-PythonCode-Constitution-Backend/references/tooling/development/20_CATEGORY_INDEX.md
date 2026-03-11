---
doc_id: "dev_pythoncode_constitution_backend.tooling.category_index"
doc_type: "index_doc"
topic: "Category index for future tooling docs of the Python backend code constitution skill"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The tooling development entry routes readers into this category index."
  - target: "modules/MODULE_TEMPLATE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Future module docs should be linked from this category index."
---

# Cli_Toolbox 开发文档分类索引

## 分类导航
- 架构与边界：`00_ARCHITECTURE_OVERVIEW.md`
- 模块清单与映射：`10_MODULE_CATALOG.yaml`
- 路由与治理：`references/routing/` 与 `references/governance/`
- Python 规则：`references/python_rules/`
- 模块文档：`modules/`
- 变更记录：`90_CHANGELOG.md`

## 分类维护规则
- 新增工具时，先更新模块目录，再补模块文档。
- 若分类结构变更，必须同步更新入口文档索引。
