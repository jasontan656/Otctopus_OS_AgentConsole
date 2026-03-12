---
doc_id: "skill_creation_template.tooling.development_entry"
doc_type: "tooling_development"
topic: "Entry document for Cli_Toolbox development references"
anchors:
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "Development work must follow the runtime contract."
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture details live in the development overview."
  - target: "Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development docs must stay in sync."
---

# Cli_Toolbox 开发文档（入口）

适用技能：`SkillsManager-Creation-Template`

## 命名约束
- 本技能内工具统一使用 `Cli_Toolbox.<tool_name>` 命名。

## 内联索引
1. 架构总览：`references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
2. 模块目录：`references/tooling/development/10_MODULE_CATALOG.yaml`
3. 分类索引：`references/tooling/development/20_CATEGORY_INDEX.md`
4. 模块文档：`references/tooling/development/modules/create_skill_from_template.md`
5. 变更记录：`references/tooling/development/90_CHANGELOG.md`

## 文档分类规则
- `Architecture`
  - 解释模板技能如何把通用治理结构收敛成统一 authoring control plane。
- `Module Catalog`
  - 记录 CLI 入口、生成器入口与职责边界。
- `Category`
  - 记录门面结构、profile、contracts、回归测试等分类索引。
- `Module Docs`
  - 单独记录生成器逻辑与回归口径。
- `Changelog`
  - 记录模板治理升级。

## 同步维护约束
- 工具变更时必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 受影响模块文档
- 若改动影响门面结构、runtime contract、profile 结构或 stage template kit，还必须同步更新：
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/governance/SKILL_AUTHORING_CONTRACT.md`
  - `references/governance/STAGED_PROFILE_REFERENCE.md`
  - `references/governance/SKILL_ARCHITECTURE_PLAYBOOK.md`
  - `references/governance/SKILL_DOCSTRUCTURE_ENFORCEMENT.md`
  - `assets/skill_template/`
  - `tests/test_create_skill_from_template_regression.py`
- `SKILL.md` 只允许保留入口、边界与导航；若细节重新长回门面，优先下沉到 references 或 contracts。
