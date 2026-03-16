---
owner: "由 `$Meta-RootFile-Manager` 作为 `Otctopus_OS_AgentConsole` repository root container 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
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
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "console_repo_runtime_contract",
    "contract_scope": "repo_root",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "read_target_contract:/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md",
      "apply_repo_local_skill_stack_for_skill_governance_turns",
      "plan_same_turn_git_traceability_if_repo_write_scope",
      "read_rootfile_governance_contract_before_repo_rootfile_edits",
      "state_write_scope_before_editing_if_write_exec"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "skills_truth_root:Skills",
      "codex_installation_root:~/.codex/skills",
      "repo_writes_require_same_turn_git_traceability",
      "skill_edits_start_from_repo_truth_source",
      "installed_skill_edits_in_codex_home_are_prohibited",
      "backend_python_governance_handoff:Dev-PythonCode-Constitution",
      "repo_rootfile_governance_uses_meta_rootfile_manager_centered_push",
      "repo_local_python_dependencies_live_in:.venv_backend_skills",
      "repo_local_frontend_dependencies_live_in:frontend_skills",
      "dependency_manifest_changes_require_lock_and_governance_sync"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_console_repo_without_file_mutation",
      "default_actions": [
        "read_repo_local_contract_before_skill_runtime_changes",
        "prefer_repo_truth_source_and_contract_output_before_audit_docs"
      ]
    },
    "WRITE_EXEC": {
      "goal": "default to full-coverage edits for the intended change",
      "default_actions": [
        "Default to full-coverage edits, proactively explore to avoid omissions, and use the meta skill stack to strengthen the result."
      ]
    }
  }
}
```

```json
{
  "domain_id": "repo_handoff",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "use_repo_truth_source_for_skill_edits",
      "route_install_sync_through_mirror_mainline",
      "installed_skill_updates_use_skillsmanager_mirror_to_codex",
      "handoff_backend_python_scope_to_dev_pythoncode_constitution",
      "handoff_repo_rootfile_governance_to_meta_rootfile_manager_centered_push",
      "skill_governance_turns_apply_repo_local_skill_stack"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "./.venv_backend_skills/bin/python3 Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": [
      "complete_git_traceability_if_repo_writes_occur",
      "run_python_lint_if_python_files_changed",
      "complete_rootfile_centered_push_and_lint_if_repo_rootfile_changed",
      "sync_dependency_lock_and_governance_mapping_if_manifest_changes_occur",
      "sync_codex_installation_after_skill_edits_when_required"
    ]
  }
}
```
</part_B>
