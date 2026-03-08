# Cli_Toolbox Usage

## 人类输入 -> 电脑动作 -> 人类输出

### `contract`
- 人类输入：想知道技能运行态总合同。
- 电脑动作：读取 `references/runtime/SKILL_RUNTIME_CONTRACT.json`，输出 machine-readable 运行合同。
- 人类输出：得到技能级规则入口、命令映射和双版本同步要求。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py contract --json | sed -n '1,200p'`

### `directive`
- 人类输入：指定 `--stage scan|collect|push`，想拿到该阶段运行指引。
- 电脑动作：读取对应阶段的 `DIRECTIVE.json`，输出 machine-readable 指引。
- 人类输出：得到该阶段的 instruction、workflow、rules；运行态不需要读 markdown。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py directive --stage scan --json | sed -n '1,200p'`

### `render-audit-docs`
- 人类输入：machine contract 已更新，需要刷新 markdown 审计版。
- 电脑动作：读取 `SKILL_RUNTIME_CONTRACT.json` 与各阶段 `DIRECTIVE.json`，重建审计用 markdown。
- 人类输出：得到被刷新的审计文档路径列表。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py render-audit-docs --json | sed -n '1,200p'`

### `scan`
- 人类输入：给一个 source root。
- 电脑动作：先抢技能内互斥锁；然后扫描该 root 下默认文档集合：`AGENTS.md`、`.gitignore`、`Octopus_CodeBase_Backend/README.md`、`Octopus_CodeBase_Backend/Deployment_Guide.md`；忽略排除目录；只写技能内部的 `scan_report.json`。
- 人类输出：得到本次扫描清单，但还没有托管副本。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py scan --source-root /home/jasontan656/AI_Projects --json | sed -n '1,240p'`

### `collect`
- 人类输入：默认消费上一步 `scan` 生成的 `scan_report.json`。
- 电脑动作：先抢技能内互斥锁；若 `scan_report.json` 缺失、为空或无条目则直接报错；否则把扫描结果里的文件完整复制进托管目录，并更新技能内部的 `registry.json` 与 `index.md`。
- 人类输出：得到当前纳管结果和托管索引页。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py collect --source-root /home/jasontan656/AI_Projects --json | sed -n '1,240p'`

### `push`
- 人类输入：指定某个目标路径或 `--all`。
- 电脑动作：先抢技能内互斥锁；若 `registry.json` 缺失、为空或无条目则直接报错；否则把技能内托管的默认文档副本回写到 registry 里的真实源路径。
- 人类输出：得到被更新的目标列表。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py push --all --json | sed -n '1,240p'`

### `registry`
- 人类输入：无，或只给 `--json`。
- 电脑动作：读取当前 `registry.json`。
- 人类输出：看到所有托管目标的源路径与托管路径映射；快速浏览优先看 `assets/managed_targets/index.md`。

示例命令（强制）：
`cd /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager && python3 scripts/Cli_Toolbox.py registry --json | sed -n '1,200p'`
