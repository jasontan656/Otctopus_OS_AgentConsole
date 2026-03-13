[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract.

<part_A>
[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `<root>/Otctopus_OS_AgentConsole/.venv_backend_skills/bin/python <root>/Otctopus_OS_AgentConsole/Skills/Disabled-Octupos-FullStack/scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "octopus_os_root" --file-kind agents --json`

2. TURN_START Contract
- if the turn will write Octopus_OS, plan same-turn Constitution lint from the start
- use the returned target contract JSON as the runtime rule source

3. Peer Read Gate
- See the returned `peer_doc` object to decide whether the same-level peer file must be read.

[EXECUTION - MANDATORY]

4. Runtime Rule Source
- The returned JSON is the runtime rule source for this path.
- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.

5. Routing
- Use the returned `routing` and `update_boundary` fields instead of reading extra markdown for runtime rules.

[TURN END - MANDATORY]

6. TURN_END Contract
- if the turn wrote Octopus_OS, run Constitution lint on the concrete target root
</part_A>

<part_B>

```json
{
  "entry_role": "octopus_os_root_runtime_entry",
  "runtime_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "audit_fields_are_not_primary_runtime_instructions": true,
    "path_metadata_is_not_action_guidance": true
  },
  "turn_start_actions": [
    "use the returned target-contract JSON as the runtime rule source",
    "classify the turn as READ_EXEC or WRITE_EXEC",
    "if the turn will write Octopus_OS, plan same-turn Constitution lint from the start",
    "treat Octopus_OS/AGENTS.md as the only external AGENTS runtime entry currently allowed in Octopus_OS"
  ],
  "runtime_constraints": [
    "treat CLI JSON as the primary runtime rule source",
    "do not use audit markdown as the primary execution guide",
    "stay within the current root-only AGENTS governance boundary",
    "all other AGENTS.md files under Octopus_OS are forbidden and must be cleaned by the AGENTS manager"
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
      "goal": "edit the governed root AGENTS mapping or trigger the manager-owned write flows",
      "default_actions": [
        "state the intended write scope before editing",
        "edit the mirror-side managed target pair instead of inventing extra external AGENTS files",
        "use mother-doc-agents-push to write back the root AGENTS and clean forbidden external AGENTS files"
      ]
    }
  },
  "active_scope_policy": {
    "governed_external_target": "/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md",
    "other_external_agents_forbidden": true,
    "current_phase": "root_only_bootstrap",
    "notes": [
      "The first governed AGENTS target is Octopus_OS/AGENTS.md.",
      "The user will continue authoring the root AGENTS content and payload from this starting point."
    ]
  },
  "forbidden_primary_runtime_pattern": [
    "Do not treat audit markdown paths as the main runtime instructions.",
    "Do not require the model to open a chain of markdown files just to learn the next command.",
    "Do not emit only path metadata when the real need is direct action guidance."
  ],
  "turn_end_actions": [
    "if the turn wrote Octopus_OS, run Constitution lint on the concrete target root",
    "if the turn changed the managed root AGENTS mapping, use mother-doc-agents-push before closing the turn"
  ]
}
```
</part_B>
