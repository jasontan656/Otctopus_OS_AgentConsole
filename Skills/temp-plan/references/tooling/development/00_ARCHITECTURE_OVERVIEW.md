# Cli_Toolbox 开发文档架构总览

适用技能：`temp-plan`

## 目标
- 显式声明本技能当前没有本地 Toolbox，避免模板生成后的占位文案误导后续维护者。
- 为未来若新增 CLI 时的治理位置预留稳定骨架。
- 记录当前真正生效的运行形态：静态参考文档 + AI维护结果目录。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 当前实现状态
- `modules: []` 是正确状态，不代表漏写。
- 运行入口由 `references/current_intent.md`、`references/application_contract.md`、`references/task_log_contract.md` 与 `references/task_log_schema.md` 组成，不依赖脚本。
- markdown 任务日志的默认落点是 `/home/jasontan656/AI_Projects/Codex_Skills_Result/temp-plan`。
- 模板资产位于 `assets/templates/`。
- 若未来补充 CLI，应新增模块文档并更新模块目录，而不是继续在本文件追加临时说明。
