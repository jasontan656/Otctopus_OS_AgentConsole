# Cli_Toolbox Usage

## 人类输入 -> 电脑动作 -> 人类输出

### `scan`
- 人类输入：给一个 source root。
- 电脑动作：先抢技能内互斥锁；然后扫描该 root 下全部 `AGENTS.md`，但忽略 `Human_Work_Zone/` 与技能自身托管目录；只写技能内部的 `scan_report.json`。
- 人类输出：得到本次扫描清单，但还没有托管副本。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py scan --source-root /home/jasontan656/AI_Projects --json | cat`

### `collect`
- 人类输入：默认消费上一步 `scan` 生成的 `scan_report.json`。
- 电脑动作：先抢技能内互斥锁；若 `scan_report.json` 缺失、为空或无条目则直接报错；否则把扫描结果里的文件完整复制进托管目录，并更新技能内部的 `registry.json` 与 `index.md`。
- 人类输出：得到当前纳管结果和托管索引页。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py collect --source-root /home/jasontan656/AI_Projects --json | cat`

### `push`
- 人类输入：指定某个目标路径或 `--all`。
- 电脑动作：先抢技能内互斥锁；若 `registry.json` 缺失、为空或无条目则直接报错；否则把技能内托管的 `AGENTS.md` 副本回写到 registry 里的真实源路径。
- 人类输出：得到被更新的目标列表。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py push --all --json | cat`

### `registry`
- 人类输入：无，或只给 `--json`。
- 电脑动作：读取当前 `registry.json`。
- 人类输出：看到所有托管目标的源路径与托管路径映射；快速浏览优先看 `assets/managed_agents/index.md`。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Agents && python3 scripts/Cli_Toolbox.py registry --json | cat`
