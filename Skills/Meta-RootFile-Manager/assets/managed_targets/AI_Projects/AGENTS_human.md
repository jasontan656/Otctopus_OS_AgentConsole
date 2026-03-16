---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_agents
doc_type: topic_atom
topic: Agents
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
owner: "由 `$Meta-RootFile-Manager` 作为 `AI_Projects` workspace root 的 runtime entry owner 负责治理；当前通过 `AGENTS_MD` 通道受管并同步这个入口文件。"
---
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
<contract>
1. 合同定位
- 本文件是 `/home/jasontan656/AI_Projects` 的运行时主合同。
- 进入任何更窄的仓库级或容器级 `AGENTS.md` 之前，先应用这份 workspace root 合同。

2. 一级读取入口
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --json`
- 每回合的 selfcheck hook 另读取：
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json`
- 若任务进入技能、技能镜像、技能安装、技能同步、技能注册、技能治理或技能运行时，再读取：
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

3. 二级分域读取
- hook_identity:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "hook_identity" --json`
- turn_start:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "turn_start" --json`
- runtime_constraints:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "runtime_constraints" --json`
- execution_modes:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "execution_modes" --json`
- repo_handoff:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "repo_handoff" --json`
- turn_end:
- `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --domain "turn_end" --json`

4. 执行约束
- 在进入具体执行前，先套用 workspace root 默认 meta runtime mainline：
- `Meta-Runtime-Selfcheck` -> `Meta-Semantic-Collection` -> `Meta-Impact-Investigation` -> `Meta-Architect-MindModel` -> `Meta-Reasoning-Chain` -> `Meta-keyword-first-edit`
- `$Meta-Runtime-Selfcheck` 是每回合常驻 runtime hook：turn start 先完成 hook arm；当本回合出现运行痛点、卡壳、命令失败、路径误用、重复试错、明显犹豫、流程迷路或局部运行不顺时，必须立即触发 selfcheck diagnose / self-repair / bounded strengthening 流程，而不是只在 final reply 前被动想起。
- `$Meta-Runtime-Selfcheck` 一旦被触发，必须先在当前边界内做最小可验证修复或局部强化，再继续主任务；若存在残余风险，必须在 final reply 前完成 selfcheck closeout 并合并进最终汇报。
- 若任务先需要把原始需求压缩成可执行意图，再先插入 `Meta-Enhance-Prompt`。
- 若任务涉及外部页面、浏览器自动化或前端 bring-up，再按任务需要追加 `Meta-Agent-Browser`。
- `READ_EXEC` / `WRITE_EXEC` 的具体行为约束继续读取 `execution_modes` 域。
- skill-related task 一旦进入 repo-local contract，repo-local 更窄协同链、mirror/install、依赖环境、lint 与 Git closeout 全部按 repo-local contract 叠加执行。
- WRITE_EXEC 进入具体写入前先声明本回合 intended write scope；除 repo-local contract 或用户明确要求外，不把 Git automation 当默认第一步。
</contract>

<reminder>
1. 环境提醒
- skills backend Python 环境位于 `/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills`。
- skills CLI 与相关 `pytest` 默认沿用同一解释器。
- 当前环境为 `WSL`；若任务确实需要系统 Python，可使用 `python3`。

2. 协作提醒
- 对话输出默认中文为主；文档写回默认中文为主、英文为辅。
- 涉及 `AGENTS.md` 时，直接展示完整绝对路径更利于核对。
- 出现与当前任务无关的并行改动时，只聚焦本任务直接相关文件。
</reminder>
</part_A>

<part_B>

```json
{
  "domain_id": "hook_identity",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"hook_identity\" --json",
  "contract": {
    "entry_role": "workspace_root_runtime_contract",
    "contract_scope": "workspace_root",
    "secondary_contract_source": "CLI_JSON"
  }
}
```

```json
{
  "domain_id": "turn_start",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"turn_start\" --json",
  "contract": {
    "required_actions": [
      "read_target_contract:/home/jasontan656/AI_Projects/AGENTS.md",
      "load_runtime_selfcheck_turn_start_contract_before_concrete_execution",
      "arm_meta_runtime_selfcheck_as_live_turn_hook_before_concrete_execution",
      "classify_turn_mode:READ_EXEC|WRITE_EXEC",
      "apply_workspace_meta_sequence_before_concrete_execution",
      "read_repo_target_contract_if_skill_task:/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md",
      "extract_current_codex_chat_session_id_on_initialization_and_cache_for_reuse"
    ]
  }
}
```

```json
{
  "domain_id": "runtime_constraints",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"runtime_constraints\" --json",
  "contract": {
    "rules": [
      "meta_runtime_selfcheck_is_mandatory_runtime_hook",
      "runtime_pain_or_unsmooth_execution_must_trigger_meta_runtime_selfcheck",
      "runtime_pain_examples:stall,tool_failure,path_misuse,retry_loop,hesitation,workflow_drift,local_unsmoothness",
      "meta_runtime_selfcheck_must_attempt_bounded_local_repair_or_strengthening_before_deferring",
      "meta_runtime_selfcheck_must_stay_active_until_final_closure",
      "cli_json_is_primary_runtime_rule_source",
      "audit_markdown_is_not_primary_execution_guide",
      "language_primary:zh-CN",
      "github_managed_repos:Octopus_OS,Otctopus_OS_AgentConsole",
      "skill_installation_mirror_repo:Otctopus_OS_AgentConsole",
      "runtime_instruction_learning_must_not_depend_on_markdown_chain"
    ]
  }
}
```

```json
{
  "domain_id": "execution_modes",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"execution_modes\" --json",
  "contract": {
    "READ_EXEC": {
      "goal": "inspect_or_route_without_file_mutation",
      "default_actions": [
        "prefer_direct_cli_contract_output_before_opening_markdown_rules",
        "open_extra_files_only_when_direct_contract_leaves_real_gap"
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
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"repo_handoff\" --json",
  "contract": {
    "rules": [
      "read_repo_local_target_contract_when_repo_agents_exists",
      "merge_workspace_root_contract_with_repo_local_contract",
      "escalate_skill_related_turns_into_repo_local_governed_mainline",
      "defer_git_automation_to_repo_local_contract_or_explicit_user_request"
    ]
  }
}
```

```json
{
  "domain_id": "turn_end",
  "read_command_preview": "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python3 /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py agents-domain-contract --source-path \"/home/jasontan656/AI_Projects/AGENTS.md\" --domain \"turn_end\" --json",
  "contract": {
    "required_actions": [
      "if_turn_has_runtime_pain_or_unsmooth_execution_trigger_meta_runtime_selfcheck_before_final_reply",
      "run_meta_runtime_selfcheck_final_closure_before_final_reply",
      "merge_meta_runtime_selfcheck_repairs_verification_and_residual_risk_into_final_reply",
      "complete_repo_local_closeout_before_final_reply",
      "reuse_current_codex_chat_session_id_and_print_it_in_every_final_reply_message"
    ]
  }
}
```
</part_B>
