# Cli_Toolbox 开发文档（入口）

适用技能：`skill-creation-template`

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
  - 解释模板技能如何把 backend 成功骨架转成通用 authoring control plane。
- `Module Catalog`
  - 记录 CLI 入口、生成器入口与职责边界。
- `Category`
  - 记录 façade、profile、contracts、回归测试等分类索引。
- `Module Docs`
  - 单独记录生成器逻辑与回归口径。
- `Changelog`
  - 记录模板治理升级。

## 同步维护约束
- 工具变更时必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 受影响模块文档
- 若改动影响 façade、runtime contract、profile 结构或 stage template kit，还必须同步更新：
  - `references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - `references/skill_template_contract_v1.md`
  - `references/staged_cli_first_profile_reference.md`
  - `references/skill_architecture_playbook.md`
  - `assets/skill_template/`
  - `tests/test_create_skill_from_template_regression.py`
- `SKILL.md` 只允许保留入口、边界与导航；若细节重新长回门面，优先下沉到 references 或 contracts。
