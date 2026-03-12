# Cli_Toolbox 使用文档

适用技能：`temp-plan`

## 当前状态
- 本技能没有本地 `Cli_Toolbox.*`。
- 本技能是纯方法论背景技能，入口是静态参考文档，不是脚本。

## 使用方式
- 读取入口：
  - `references/current_intent.md`
  - `references/application_contract.md`
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
- 若未来新增工具，必须同步更新本文件、`Cli_Toolbox_DEVELOPMENT.md`、模块目录与模块文档。
