[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

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
