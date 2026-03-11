---
doc_id: "skill_creation_template.index.tooling_category_index"
doc_type: "index_doc"
topic: "Category index for Cli_Toolbox development references"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "This index is linked from the development entry."
  - target: "../../indexes/DOC_TREE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "The broader doc tree complements this tooling-specific index."
  - target: "modules/create_skill_from_template.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The category index routes readers into module docs."
---

# Cli_Toolbox 开发文档分类索引

## 分类导航
- `统一入口`
  - `scripts/Cli_Toolbox.py`
- `门面与合同`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/governance/SKILL_AUTHORING_CONTRACT.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
- `复杂 staged profile`
  - `references/governance/STAGED_PROFILE_REFERENCE.md`
  - `assets/skill_template/SKILL_TEMPLATE_STAGED.md`
  - `assets/skill_template/stages/`
- `基础 profile`
  - `assets/skill_template/SKILL_TEMPLATE.md`
- `模块清单与映射`
  - `10_MODULE_CATALOG.yaml`
- `模块文档`
  - `modules/create_skill_from_template.md`
  - `modules/MODULE_TEMPLATE.md`
- `回归测试`
  - `tests/test_create_skill_from_template_regression.py`
- `变更记录`
  - `90_CHANGELOG.md`

## 分类维护规则
- 新增工具时，先补 `10_MODULE_CATALOG.yaml` 再补模块文档。
- 若新增模板 profile 或合同面，必须同步更新本索引。
- 若回归测试口径变化，必须把测试入口保留在本索引中。
