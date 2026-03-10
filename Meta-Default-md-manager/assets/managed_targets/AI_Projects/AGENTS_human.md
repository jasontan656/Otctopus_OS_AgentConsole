[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

[PART A]

1. 根入口命令
- 在处理 workspace root 路径规则之前，必须先运行：
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --json`

2. 语言规范
- 对话输出必须使用中文为主。
- 起草与写回文档时默认使用中文为主，英文为辅。
- 英文只用于技术栈、路径、命令、环境变量、API 名、函数名、类名与其他工程向标识符。

3. 当前受管 repo 边界
- `$meta-github-operation` 当前仅管理以下 repo：
- `Octopus_OS`
- `Codex_Skills_Mirror`

4. Multi-AGENT 工作模式
- Multi-AGENT work mode 下，同一文件夹在工作过程中可能出现未预期的并行改动。
- 当出现与当前任务无关的并行变更时，应忽略这些无关变更，只关注与当前任务直接相关的文件。
5. AGENTS 协同更新约束
- 当更新 `AGENTS.md` 的内容时，必须一同检查并同步对应的 `md + json + cli`。
- 如果字段 shape 或 payload 结构发生变化，必须一同更新 CLI 输出与相关 machine-readable JSON。
