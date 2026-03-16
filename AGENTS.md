---
owner: "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 当前可用的 repo-local skills backend Python 虚拟环境为：`./.venv_backend_skills`。
- 运行 repo-local skills CLI 时，优先使用：`./.venv_backend_skills/bin/python3`。
- 在处理 `Otctopus_OS_AgentConsole` 路径规则之前，必须先运行：
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

2. 当前受管 repo 身份
- Current concrete repo: `Otctopus_OS_AgentConsole`
- Current target kind: `AGENTS.md`
- `AGENTS.md` 应保持为 thin runtime entry；具体 routing/update 规则以返回的 JSON contract 为准。
- same-level `README.md` 已可用，可作为对外产品摘要入口。

3. Repo-local skills 依赖环境
- 与 skills 执行相关的 Python 依赖环境固定为 `./.venv_backend_skills`；对应锁文件为 `./requirements-backend_skills.lock.txt`。
- 若需要运行 `pytest` 验证 skills 或 backend Python 相关改动，优先使用：`./.venv_backend_skills/bin/python3 -m pytest`。
- 与 skills 执行相关的前端依赖环境固定为 `./frontend_skills/`；对应真源为 `package.json` 与 `package-lock.json`。
- 若需要新增 repo-local 依赖，安装位置只能是本 repo 的 `*_skills` 环境或其受管 manifest/lock 所在目录，不得把全局环境当长期依赖承载层。

4. 同回合收口
- 如果本回合写入 `Otctopus_OS_AgentConsole`，必须同回合完成 Git traceability。
- 若任务内容涉及 Python 相关编辑，结束前必须完成 `Dev-PythonCode-Constitution` 的 lint。
</part_A>
