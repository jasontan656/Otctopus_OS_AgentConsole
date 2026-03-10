[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

[PART A]

1. 根入口命令
- 在处理 workspace root 路径规则之前，必须先运行：
- `command_replace_me`

[PART B]

```json
{
  "entry_role": "workspace_root_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "turn_start_actions": [
    "validate root AGENTS exists",
    "classify the turn as READ_EXEC or WRITE_EXEC"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "when a concrete repo path becomes active, load that repo-local contract before repo-specific write, lint, or Git actions"
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
      "default_must_use": [
        "$Meta-github-operation (Any file write must leave trace in github by pushing changes to main)"
      ],
      "default_actions": [
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
    "defer repo-specific lint or Git duties to the concrete repo-local contract when applicable"
  ]
}
```
