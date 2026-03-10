# Target Rule Audit

> Human audit copy generated from the skill-managed target runtime JSON.
> Runtime models must call the CLI listed below instead of reading this markdown.

## Target
- source_path: `/home/jasontan656/AI_Projects/AGENTS.md`
- target_kind: `AGENTS.md`
- managed_rel_path: `home_jasontan656_AI_Projects/AGENTS.md`

## Runtime Entry
- cli: `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/AGENTS.md" --json`
- runtime_json_path: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/home_jasontan656_AI_Projects/AGENTS_machine.json`

## Peer Doc
- path: `/home/jasontan656/AI_Projects/README.md`
- read_policy: `not_available`

## Turn Contract
- status: `enforced`
- turn_start:
  - validate /home/jasontan656/AI_Projects/AGENTS.md exists
  - print TURN_START guardrails
  - print ROUTE guardrails
  - choose READ_EXEC or WRITE_EXEC by write intent
- turn_end:
  - print TURN_END guardrails
