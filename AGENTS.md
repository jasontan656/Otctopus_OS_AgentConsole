[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 `Codex_Skills_Mirror` 路径规则之前，必须先运行：
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/AGENTS.md" --json`

2. 当前受管 repo 边界
- Current concrete repo: `Codex_Skills_Mirror`
- Current target kind: `AGENTS.md`
- `AGENTS.md` 应保持为 thin runtime entry；具体 routing/update 规则以返回的 JSON contract 为准。
- same-level `README.md` 当前不可用，不需要作为同级摘要入口。

3. Runtime Rule Source
- CLI JSON 输出是该路径的运行时规则源。
- skill 内部 markdown 审计文件仅供人类审计，不可替代 CLI JSON。

4. 同回合要求
- 如果本回合写入 `Codex_Skills_Mirror`，必须从一开始就纳入 Constitution lint 与 Git traceability。
- 结束前必须完成 concrete repo 的 Constitution lint。
- 如果本回合写入了 `Codex_Skills_Mirror`，必须同回合 commit-and-push。
</part_A>
