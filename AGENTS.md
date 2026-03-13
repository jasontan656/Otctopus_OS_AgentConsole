---
owner: "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 `Otctopus_OS_AgentConsole` 路径规则之前，必须先运行：
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

2. 当前受管 repo 身份
- Current concrete repo: `Otctopus_OS_AgentConsole`
- Current target kind: `AGENTS.md`
- `AGENTS.md` 应保持为 thin runtime entry；具体 routing/update 规则以返回的 JSON contract 为准。
- same-level `README.md` 已可用，可作为对外产品摘要入口。

3. Runtime Rule Source
- CLI JSON 输出是该路径的运行时规则源。
- `Part B` 负责 machine payload；skills 治理顺序与最小语义入口以 `default_meta_skill_order` 为准。
- 路径、语言、依赖、tech stack、mirror/install、Git traceability 等具体规则若已在 `Part B` 或对应 `SkillsManager` 技能内声明，不在 `Part A` 重复展开。

4. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>
