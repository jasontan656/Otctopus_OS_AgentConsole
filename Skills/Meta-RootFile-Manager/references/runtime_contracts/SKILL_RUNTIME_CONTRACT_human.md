# Skill Runtime Contract Human Mirror

## 主入口
- `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py contract --json`

## AGENTS 相关入口
- 日常维护：
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-maintain --intent "<natural language request>" --json`
- 目标整体合同：
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "<external AGENTS path>" --json`
- 单域二级合同：
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "<external AGENTS path>" --domain "<domain_id>" --json`
- 窄域 block surgery：
  `./.venv_backend_skills/bin/python Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-payload-contract --source-path "<external AGENTS path>" --json`

## 当前治理形态
- 外部 `AGENTS.md` 是完整合同正文加 reminder 尾部。
- 内部 `AGENTS_human.md` 是完整合同真源，并携带多块分域 machine contract。
- `collect` 不再属于 AGENTS 日常维护主链。
