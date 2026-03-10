[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --json`

2. TURN_START Contract
- validate /home/jasontan656/AI_Projects/AGENTS.md exists
- print TURN_START guardrails
- print ROUTE guardrails
- choose READ_EXEC or WRITE_EXEC by write intent

3. Peer Document Gate
- See the returned `peer_doc` object to decide whether the same-level peer file exists and whether it must be read.

[EXECUTION - MANDATORY]

4. Runtime Rule Source
- The CLI JSON output is the runtime rule source for this path.
- Skill-internal markdown audit files are for human audit only; models must not treat them as runtime guidance.

5. Managed Boundary
- Current target kind: `AGENTS.md`.
- `AGENTS.md` should remain a thin runtime entry; concrete routing/update rules live in the returned JSON contract.

[GLOBAL LANGUAGE - MANDATORY]

6. Language Constraint
- Unless the user explicitly asks for a pure translation task, replies and writeback content must be Chinese-first.
- English is secondary and should be limited to engineering-facing content such as tech stacks, file paths, commands, environment variables, API names, function names, class names, schema keys, and other code-native identifiers.
- Do not switch the main narrative language away from Chinese just because the user mixes in English.

[TURN END - MANDATORY]

7. TURN_END Contract
- print TURN_END guardrails
