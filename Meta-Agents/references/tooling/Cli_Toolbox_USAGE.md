# Cli_Toolbox Usage

## 人类输入 -> 电脑动作 -> 人类输出

### `scan-collect`
- 人类输入：给一个 source root。
- 电脑动作：扫描该 root 下全部 `AGENTS.md`，但忽略 `Human_Work_Zone/` 与技能自身托管目录；其余命中的文件会被完整复制进 `assets/managed_agents/`，并更新 `registry.json`。
- 人类输出：得到当前纳管文件清单与托管副本路径。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py scan-collect --source-root /home/jasontan656/AI_Projects --json | cat`

### `sync-out`
- 人类输入：指定某个目标路径或 `--all`。
- 电脑动作：把技能内托管的 `AGENTS.md` 副本回写到 registry 里的真实源路径。
- 人类输出：得到被更新的目标列表。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py sync-out --all --json | cat`

### `registry`
- 人类输入：无，或只给 `--json`。
- 电脑动作：读取当前 `registry.json`。
- 人类输出：看到所有托管目标的源路径与托管路径映射。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py registry --json | cat`
