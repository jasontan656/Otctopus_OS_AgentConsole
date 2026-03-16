# Cli_Toolbox 使用文档

适用技能：`temp-plan`

## 当前状态
- 本技能没有本地 `Cli_Toolbox.*`。
- 本技能通过 AI 直接维护 markdown 任务日志，不依赖本地脚本。

## 使用方式
- 读取入口：
  - `references/current_intent.md`
  - `references/application_contract.md`
  - `references/task_log_contract.md`
  - `references/task_log_schema.md`
- 默认结果根：
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/temp-plan`
- 默认模板资产：
  - `assets/templates/ACTIVE_TASK.template.md`
  - `assets/templates/TASK.template.md`
  - `assets/templates/TURN_LOG.template.md`
- 若任务需要真正创建或安装技能，转由其他技能处理：
  - 模板治理：`$SkillsManager-Creation-Template`
  - 镜像安装：`$SkillsManager-Mirror-To-Codex`

## 命令说明
- 当前无示例命令。
- 若未来为本技能补充本地 CLI，必须同步新增：
  - 工具清单
  - 一行可复制示例命令
  - 参数与输出契约
  - 对应开发文档

## 同步维护要求
- 若本技能仍保持“无本地 CLI”状态，本文件应明确写清 absence，不得留下模板占位语。
- 即使无 CLI，也要同步维护结果根、模板资产与任务日志合同说明。
