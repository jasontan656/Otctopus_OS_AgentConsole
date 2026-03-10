[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md" --json`

2. TURN_START Contract
- N/A

3. Peer Document Gate
- If the returned payload includes `peer_summary_policy`, use it to decide whether the same-level README summary exists and whether it should be read.

[EXECUTION - MANDATORY]

4. Runtime Rule Source
- The CLI JSON output is the runtime rule source for this path.
- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.

5. Managed Boundary
- Current target kind: `AGENTS.md`.
- `AGENTS.md` should remain a thin runtime entry; concrete routing/update rules live in the returned JSON contract.

[TURN END - MANDATORY]

6. TURN_END Contract
- N/A

7. Peer Summary Policy
- same-level README.md is a human summary; read it only when the current task needs that summary

[PART B]

```json
{
  "entry_role": "repo_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "default_meta_skill_order": [
    "$Meta-prompt-write (strengthen user intent and understand the real need)",
    "$Meta-mindchain (think from the architecture level and reject one-sided thinking)",
    "$Meta-reasoningchain (project the future shape to align the target state)",
    "$Meta-keyword-first-edit (prefer delete > replace > add when editing)",
    "$Meta-refactor-behavior-preserving (applicable only when refactor is needed)",
    "$Meta-Agent-Browser (applicable only when the task is frontend or browser-related)"
  ],
  "peer_summary_policy": {
    "available": true,
    "relation": "same_level_summary",
    "read_policy": "optional_then_required_on_write_if_exists",
    "guidance": "same-level README.md is a human summary; read it only when the current task needs that summary"
  },
  "turn_start_actions": [
    "use the returned target contract JSON as the runtime rule source"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the concrete repo-local boundary defined by this payload",
    "same-level README.md remains a human summary; read it only when the current task needs that extra context"
  ],
  "turn_end_actions": [
    "follow repo-specific lint or Git duties only when they are explicitly listed in this payload"
  ],
  "repo_name": "Octopus_CodeBase_Frontend"
}
```
