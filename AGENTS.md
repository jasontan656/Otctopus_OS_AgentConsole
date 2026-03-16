[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole` 的仓库根运行时合同。
- 凡是技能真源、技能目录、技能运行时、受管 root files 与 mirror/sync 主链相关的写入，都先应用这份 repo root 合同。

2. 一级读取入口
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

3. 二级分域读取
- hook_identity:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- skill-related turn 进入本合同后，先按 repo-local skill stack 协同推进：
- `SkillsManager-Naming-Manager` -> `SkillsManager-Creation-Template` -> `SkillsManager-Doc-Structure` -> `SkillsManager-Tooling-CheckUp`
- 若任务已落到 codex 安装侧同步，同回合追加 `SkillsManager-Mirror-To-Codex`。
- 若任务发生 repo write，同回合追加 `Meta-github-operation`，并在收口前完成同回合 Git traceability。
- 若任务包含 backend-side Python 编辑、Python runtime 依赖调整或 repo-local Python 环境调整，同回合追加 `Dev-PythonCode-Constitution`。
- 若任务是新 skill 创建或大改 skill facade，再按需追加 `Skill-creator`。
- skill edit 只从 `Otctopus_OS_AgentConsole/Skills/` repo truth source 起步，不在 `~/.codex/skills` 直接改真源。
- 已安装 skill 的改动完成后，同回合通过 `SkillsManager-Mirror-To-Codex` 向 codex 安装侧同步；安装侧不存在的新 skill 走 install，已存在的 skill 走 push。
- 若任务治理当前 repo 的 `AGENTS.md` 或其他 repo root 受管 root files，必须通过 `Meta-RootFile-Manager` 的 internal truth -> centered push -> lint 主链完成；`collect` 只保留 reverse-sync / recovery。
- 依赖环境、manifest/lock、governance mapping 与 closeout 细则继续读取 `runtime_constraints`、`repo_handoff` 与 `turn_end` 域。
</contract>

<reminder>
1. 环境提醒
- repo-local skills backend Python 环境位于 `./.venv_backend_skills`。
- repo-local skills CLI 与相关 `pytest` 默认沿用同一解释器。
- repo-local frontend skills 依赖位于 `./frontend_skills/`；只有任务确实进入前端 skill runtime 时才需要用到。

2. 协作提醒
- 同级 `README.md` 只承接仓库说明与目录边界。
- 若任务确实需要同步到 `~/.codex/skills`，沿用 mirror 主链；不在安装侧直接扩写真源语义。
</reminder>
