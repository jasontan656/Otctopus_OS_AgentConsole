---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_agents
doc_type: topic_atom
topic: Agents
anchors:
- target: ../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
---

[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
1. 根入口命令
- 在处理 workspace root 路径规则之前，必须先运行：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --json`

2. 技能类任务附加入口
- 任何时候只要任务涉及技能、技能镜像、技能安装、技能同步、技能注册、技能治理或技能运行时，必须阅读：
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Meta-RootFile-Manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md" --json`

3. 语言规范
- 对话输出必须使用中文为主。
- 起草与写回文档时默认使用中文为主，英文为辅。
- 英文只用于技术栈、路径、命令、环境变量、API 名、函数名、类名与其他工程向标识符。

4. 当前受管 repo 边界
- `$meta-github-operation` 当前仅管理以下 repo：
- `Octopus_OS`
- `Otctopus_OS_AgentConsole`
- `Otctopus_OS_AgentConsole` 仍承担与 `~/.codex/skills` 的受控映射关系

5. Multi-AGENT 工作模式
- Multi-AGENT work mode 下，同一文件夹在工作过程中可能出现未预期的并行改动。
- 当出现与当前任务无关的并行变更时，应忽略这些无关变更，只关注与当前任务直接相关的文件。

6. 治理链约束
- 更新本文件时及相关内容时,必须使用 $Meta-RootFile-Manager 更新治理映射模版然后再回推至本文件,或者更新本文件但是必须使用技能的collect来反向更新,避免单点更新治理链断裂.
</part_A>

<part_B>

```json
{
  "entry_role": "workspace_root_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Meta-Semantic-Collection (understand human expressed meaning and update it according to its rule)",
    "$Meta-Enhance-Prompt (strengthen user intent and understand the real need)",
    "$Meta-Impact-Investigation (ensure the coverage of user request before conclusion or edits)",
    "$Meta-Architect-MindModel (think from the architecture level and reject one-sided thinking)",
    "$Meta-reasoningchain (project the future shape to align the target state)",
    "$Meta-keyword-first-edit (prefer delete > replace > add when editing)",
    "$Meta-Agent-Browser (applicable only when the task is frontend or browser-related)"
  ],
  "turn_start_actions": [
    "validate root AGENTS exists",
    "if the task is skill-related, load the repo-local target contract for /home/jasontan656/AI_Projects/Otctopus_OS_AgentConsole/AGENTS.md before skill-specific actions",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "apply the default meta sequence before concrete execution"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "for any skill-related task, load the Otctopus_OS_AgentConsole repo-local contract before skill-specific reads, writes, sync, install, registry, lint, or Git actions",
    "when a concrete repo path becomes active, load that repo-local contract before repo-specific write, lint, or Git actions",
    "before every final reply, hard-execute the Meta-Runtime-Selfcheck turn-end hook instead of treating selfcheck as optional narration",
    "the turn-end hook itself must run every turn for analysis; only the extra selfcheck output may be skipped when the run is smooth"
  ],
  "execution_modes": {
    "READ_EXEC": {
      "goal": "answer, inspect, classify, or route without changing files",
      "default_actions": [
        "prefer direct CLI contract output over opening markdown rule files",
        "open extra files only when the direct contract still leaves a real gap"
      ]
    },
    "WRITE_EXEC": {
      "goal": "edit files or trigger manager-owned write flows",
      "default_actions": [
        "apply the default meta sequence before editing",
        "state the intended write scope before editing",
        "edit the minimal correct scope that matches the user intent",
        "do not trigger Git automation unless the active repo-local contract or the user explicitly requires it"
      ]
    }
  },
  "repo_local_contract_handoff": [
    "if work enters a repo with its own AGENTS runtime entry, load that repo-local target-contract before following repo-specific rules",
    "repo-local contract may add stricter lint, delivery, or Git rules for that repo only",
    "when repo-local and workspace-root rules overlap, keep the workspace-root boundary and add the repo-local concrete duties"
  ],
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
    "Do not emit only path metadata when the real need is direct action guidance."
  ],
  "turn_end_actions": [
    "print TURN_END guardrails",
    "hard-execute the $Meta-Runtime-Selfcheck turn-end hook before final reply",
    "run the turn-end hook analysis on every turn; do not skip the hook itself just because the run looks smooth",
    "call runtime-contract --json first, then read directive --topic turn-end-selfcheck --json as the default branch",
    "if the run is smooth, skip only the extra selfcheck output and continue to the normal final reply",
    "if issues are present, classify them into immediate same-turn repair, optimization guidance, and unresolved risk",
    "when a bounded fix is safe within the active repo boundary, repair first; otherwise merge concise selfcheck findings into the same final reply",
    "defer repo-specific lint or Git duties to the concrete repo-local contract when applicable"
  ]
}
```
</part_B>
