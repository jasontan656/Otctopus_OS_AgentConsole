# Target Rule Audit

> Human audit copy generated from the skill-managed target runtime JSON.
> Runtime models must call the CLI listed below instead of reading this markdown.

## Target
- source_path: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/AGENTS.md`
- target_kind: `AGENTS.md`
- managed_rel_path: `AI_Projects/Codex_Skills_Mirror/AGENTS.md`

## Runtime Entry
- cli: `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/AGENTS.md" --json`
- runtime_json_path: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Codex_Skills_Mirror/AGENTS_machine.json`

## Peer Doc
- path: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/README.md`
- read_policy: `not_available`

## Turn Contract
- status: `enforced`
- turn_start:
  - use the returned target contract JSON as the runtime rule source
  - if the turn will write Codex_Skills_Mirror, plan same-turn Constitution lint and Git traceability from the start
- turn_end:
  - run Constitution lint on the concrete Codex_Skills_Mirror target root
  - if the turn wrote Codex_Skills_Mirror, complete same-turn commit-and-push before closing the turn
