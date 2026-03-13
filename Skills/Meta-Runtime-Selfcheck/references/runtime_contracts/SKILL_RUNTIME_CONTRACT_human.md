---
doc_id: "meta_runtime_selfcheck.runtime_contract"
doc_type: "topic_atom"
topic: "CLI-first runtime contract for Meta-Runtime-Selfcheck"
node_role: "topic_atom"
domain_type: "runtime_contract"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "The runtime contract is the first governed runtime branch linked from the facade."
  - target: "DIAGNOSE_WORKFLOW_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Turn-end selfcheck selection follows the runtime contract."
  - target: "FINAL_REPLY_MERGE_CONTRACT_human.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Runtime findings must be merged into the same final reply."
---

# SKILL_RUNTIME_CONTRACT

<part_A>
- 人类阅读时可用本文件理解 `Meta-Runtime-Selfcheck` 的 CLI-first 入口。
- 本技能当前不是“只有手动点名才进入”的后置复盘器，而是默认 `turn end` 自检合同。
- 当任务进入具体自检、自修或 final reply 合并语境时，再读取对应 directive。
</part_A>

<part_B>

```json
{
  "contract_name": "meta_runtime_selfcheck_runtime_contract",
  "contract_version": "2.0.0",
  "skill_name": "__SKILL_NAME__",
  "runtime_source_policy": {
    "primary_runtime_source": "CLI_JSON",
    "human_markdown_role": "part_a_narrative_for_humans",
    "payload_role": "part_b_json_for_models",
    "markdown_is_not_primary_instruction_source": true
  },
  "trigger_policy": {
    "default_trigger": "turn_end",
    "manual_invoke_still_allowed": true,
    "skip_when_smooth": true,
    "allow_implicit_invocation": true
  },
  "tool_entry": {
    "script": "scripts/Cli_Toolbox.py",
    "commands": {
      "runtime-contract": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py runtime-contract --json",
      "directive": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py directive --topic <topic> --json",
      "paths": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json",
      "diagnose": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py \">\" --session-scope-mode all_threads --max-results 200",
      "repair": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/runtime_pain_batch.py 修复 --manual-repair-applied --manual-repair-path <changed_file> --verify-cmd <verify_cmd>"
    }
  },
  "must_use_sequence": [
    "Near turn end, call runtime-contract before consuming runtime guidance for this skill.",
    "Read the turn-end-selfcheck directive as the default branch.",
    "If issues are detected, decide whether same-turn self-repair is safe; otherwise downgrade the item into final-reply optimization guidance.",
    "Call paths --json when governed runtime or result paths matter.",
    "Open human mirrors only when the direct JSON payload still leaves a real gap."
  ],
  "directive_topics": [
    {
      "topic": "turn-end-selfcheck",
      "doc_kind": "workflow",
      "use_when": "Every turn end before final reply; skip output if the run is smooth."
    },
    {
      "topic": "self-repair-writeback",
      "doc_kind": "contract",
      "use_when": "Turn-end selfcheck found a bounded issue that can be safely repaired and verified in the same turn."
    },
    {
      "topic": "output-governance",
      "doc_kind": "contract",
      "use_when": "The task needs governed runtime log roots, result roots, or repair-evidence artifact policy."
    },
    {
      "topic": "final-reply-merge",
      "doc_kind": "contract",
      "use_when": "The turn found optimization items or self-repair outcomes that must be merged into the same final reply."
    }
  ],
  "runtime_dependencies": {
    "pain_provider": {
      "environment_variable": "CODEX_RUNTIME_PAIN_PROVIDER",
      "cli_override": "--memory-runtime <provider.py>",
      "required_for": [
        "diagnose",
        "repair"
      ],
      "fallback_policy": "If unavailable, perform a lightweight selfcheck from the visible turn evidence instead of failing the user-facing answer."
    },
    "history_source": {
      "default_path": "__DEFAULT_HISTORY_PATH__",
      "environment_override": "CODEX_HOME"
    }
  },
  "path_policy": {
    "runtime_log_root_rule": "__RUNTIME_ROOT__/logs/runtime_pain_batch/<run_id>",
    "result_root_rule": "__RESULT_ROOT__",
    "resolved_paths_command": "./.venv_backend_skills/bin/python Skills/Meta-Runtime-Selfcheck/scripts/Cli_Toolbox.py paths --json"
  },
  "hard_constraints": [
    "Use this skill near turn end by default, not only when the user manually invokes it.",
    "Skip selfcheck output when the turn was smooth and the extra section would be noise.",
    "Do not treat SKILL.md as the primary runtime instruction source.",
    "Do not perform speculative broad auto-repairs under the name of selfcheck.",
    "Do not default logs or result artifacts to the current working directory."
  ]
}
```
</part_B>
