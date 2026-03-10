# Cli_Toolbox 开发文档（入口）

适用技能：`meta-topic-anchor-graph`

## 当前状态
- `v1` 没有 CLI，也没有 runtime contract 脚本。
- 当前实现以 markdown contract + templates 为主，不以工具为主。

## 阅读顺序
1. `references/topic-anchor-graph-contract.md`
2. `assets/templates/ROOT_INDEX_TEMPLATE.md`
3. `assets/templates/TOPIC_ATOM_TEMPLATE.md`
4. `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`

## 开发约束
- 若未来引入工具，必须先定义：
  - 输入输出合同
  - anchor 结构是否 machine-readable
  - tooling 文档同步策略
- 新增工具时，必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - `references/tooling/development/20_CATEGORY_INDEX.md`
  - 对应模块文档
