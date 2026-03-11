# Cli_Toolbox Usage

Applies to skill: `production-form`

## Tools
- `Cli_Toolbox.working_contract`
- `Cli_Toolbox.intent_snapshot`
- `Cli_Toolbox.latest_log`
- `Cli_Toolbox.append_iteration_log`

## Narrative Usage

### `Cli_Toolbox.working_contract`
- Human intent:
  - "Tell me the current operating contract of this temporary product-form skill."
- Machine action:
  - Read `references/runtime/WORKING_CONTRACT.json`.
- Output:
  - Contract payload, current mission, hard boundaries, and local history paths.

### `Cli_Toolbox.intent_snapshot`
- Human intent:
  - "Show me what this product is currently trying to become."
- Machine action:
  - Read `references/runtime/CURRENT_PRODUCT_INTENT.md`.
- Output:
  - The current Octopus OS product intent snapshot.

### `Cli_Toolbox.latest_log`
- Human intent:
  - "Show me the latest local product-form history before we continue."
- Machine action:
  - Read the latest section(s) from `references/runtime/ITERATION_LOG.md`.
- Output:
  - The most recent local design-log entries.

### `Cli_Toolbox.append_iteration_log`
- Human intent:
  - "Record the new product-shaping decision we just made."
- Machine action:
  - Append a structured markdown entry to `references/runtime/ITERATION_LOG.md`.
- Output:
  - Timestamp, log path, and appended entry title.

## Example Commands
- Load working contract:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/production-form && python3 scripts/Cli_Toolbox.py working-contract --json | sed -n '1,200p'`
- Load current intent snapshot:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/production-form && python3 scripts/Cli_Toolbox.py intent-snapshot --json | sed -n '1,200p'`
- Load latest log:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/production-form && python3 scripts/Cli_Toolbox.py latest-log --json | sed -n '1,200p'`
- Append a new local design log entry:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/production-form && python3 scripts/Cli_Toolbox.py append-iteration-log --title "Refine installer boundary" --summary "Locked the temporary install boundary between product surfaces and codex skill roots." --decision "Keep product docs outside ~/.codex/skills" --affected-path "product_tools/octopus_os_agent_console.py" --next-step "Fold the new rule into the public install flow" --json | sed -n '1,200p'`
