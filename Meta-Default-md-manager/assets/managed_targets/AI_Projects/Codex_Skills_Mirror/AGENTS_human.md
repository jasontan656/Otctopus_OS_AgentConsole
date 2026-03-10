[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/AGENTS.md" --json`

2. TURN_START Contract
- use the returned target contract JSON as the runtime rule source
- if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start

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
- run Constitution lint on the concrete Codex_Skills_Mirror target root
- if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn

7. Peer Summary Policy
- same-level README.md is not available for this target
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
  "document_semantic_standard": [
    "single document, single semantic theme",
    "one theme must preserve one responsibility, one boundary, one consumer, and one runtime layer",
    "document body may explain only its own rules, structure, constraints, inputs, and outputs",
    "adjacent themes may be referenced only by pointer, not expanded inline",
    "split action semantics away from object semantics",
    "split content structure semantics away from stage semantics",
    "split governance rules away from tool definitions"
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
    "when this repo will be written, keep same-turn Constitution lint and Git traceability in scope from the start"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the concrete Codex_Skills_Mirror repo boundary defined by this payload",
    "choose READ_EXEC or WRITE_EXEC by actual write intent, not by file type alone",
    "when this repo is written, keep same-turn Constitution lint and Git traceability in scope"
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
    "if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn"
  ],
  "repo_name": "Codex_Skills_Mirror"
}
```
</part_B>
