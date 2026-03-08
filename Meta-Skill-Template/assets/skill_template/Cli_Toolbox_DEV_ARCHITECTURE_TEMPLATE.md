# Cli_Toolbox 开发文档架构总览

适用技能：`${skill_name}`

## 目标
- 用结构化文档支撑复杂 Toolbox，而不是依赖单一开发文档。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 额外要求
- 若技能存在运行态规则、约束、指引，开发架构必须明确 machine-readable 合同、CLI 输出入口与 markdown 审计版的关系。
