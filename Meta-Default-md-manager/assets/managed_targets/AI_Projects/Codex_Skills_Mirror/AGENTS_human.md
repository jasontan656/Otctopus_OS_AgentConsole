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
- 如果本回合编辑 skill，必须先在 `Codex_Skills_Mirror` 中的 mirror 副本完成编辑，禁止直接编辑 codex 安装目录下的对应 skill。
- skill 编辑完成后，若目标 skill 已存在于 codex 安装目录，必须同回合执行 `$skill-mirror-to-codex` 的 `Push`；若目标 skill 是新建且 codex 安装目录中尚不存在，必须同回合执行 `$skill-mirror-to-codex` 的 `Install`。
- 结束前必须完成 concrete repo 的 Constitution lint。
- 如果本回合写入了 `Codex_Skills_Mirror`，必须同回合 commit-and-push。
</part_A>

<part_B>

```json
{
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$meta-github-operation (after any write to Codex_Skills_Mirror, commit-and-push the mirror repo for Git traceability; Git push is not a substitute for syncing the codex installation directory)",
    "$skill-mirror-to-codex (edit skills only in Codex_Skills_Mirror mirror paths, never directly in the codex installation directory; after editing, use Push for already-installed skills and Install for newly created skills)",
    "$Meta-Skill-Template ( should be considered to imply if there is no specific user request on how skill should be created (prioritize user request than template) )",
    "$skill-creator (for skill standard formatter to ensure codex reads it properly, do not use its template for skill creation)",
    "$Constitution-knowledge-base (for skill CLI tool lints )"
  ],
  "peer_summary_policy": {
    "available": false,
    "relation": "same_level_summary",
    "read_policy": "not_available",
    "guidance": "same-level README.md is not available for this target"
  },
  "turn_start_actions": [
    "use the returned target contract JSON as the runtime rule source",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start",
    "if the turn will edit a skill, treat the mirror copy in Codex_Skills_Mirror as the only editable source and determine whether downstream sync must be Push or Install"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the concrete repo-local boundary defined by this payload",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "when this repo is written, keep same-turn Constitution lint and Git traceability in scope",
    "for skill changes, edit the mirror copy under Codex_Skills_Mirror and never directly edit the codex installation directory",
    "after skill edits, use skill-mirror-to-codex Push for already-installed skills or Install for newly created skills before closing the turn"
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
        "for skill edits, write only the mirror copy under Codex_Skills_Mirror and do not directly edit the codex installed copy",
        "after skill edits, run skill-mirror-to-codex Push for existing installed skills or Install for newly created skills",
        "run Constitution lint on Codex_Skills_Mirror before closing the turn",
        "complete same-turn commit-and-push when Codex_Skills_Mirror files are written"
      ]
    }
  },
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not require the model to open a chain of markdown files just to learn the next skill to use.",
    "Do not emit only path metadata when the real need is direct action guidance."
  ],
  "turn_end_actions": [
    "run Constitution lint on the concrete Codex_Skills_Mirror target root",
    "if the turn edited a skill, complete skill-mirror-to-codex Push or Install before closing the turn",
    "if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn"
  ],
  "repo_name": "Codex_Skills_Mirror"
}
```
</part_B>
