# Cli_Toolbox Usage

Applies to skill: `skill-production-form`

## Tools
- `Cli_Toolbox.working_contract`
- `Cli_Toolbox.intent_snapshot`
- `Cli_Toolbox.latest_log`
- `Cli_Toolbox.append_iteration_log`

## Narrative Usage

### `Cli_Toolbox.working_contract`
- Human intent:
  - "Tell me the current operating contract of this console product-form skill."
- Machine action:
  - Read `references/runtime/WORKING_CONTRACT.json`.
- Output:
  - Contract payload, current mission, hard boundaries, and local history paths.

### `Cli_Toolbox.intent_snapshot`
- Human intent:
  - "Show me what this console directory is currently trying to become."
- Machine action:
  - Read `references/runtime/CURRENT_PRODUCT_INTENT.md`.
- Output:
  - The current console-productization intent snapshot.

### `Cli_Toolbox.latest_log`
- Human intent:
  - "Show me the latest local console-productization history before we continue."
- Machine action:
  - Read the latest section(s) from `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form/ITERATION_LOG.md`.
  - If the governed runtime log does not exist yet, seed it from `references/runtime/ITERATION_LOG.md` first.
- Output:
  - The most recent local design-log entries.

### `Cli_Toolbox.append_iteration_log`
- Human intent:
  - "Record the new console-productization decision we just made."
- Machine action:
  - Append a structured markdown entry to `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form/ITERATION_LOG.md`.
- Output:
  - Timestamp, runtime root, result root, log path, and appended entry title.

## Runtime And Output Governance
- Runtime observability root:
  - `/home/jasontan656/AI_Projects/Codex_Skill_Runtime/skill-production-form`
- Result root:
  - `/home/jasontan656/AI_Projects/Codex_Skills_Result/skill-production-form`
- Legacy seed snapshot:
  - `references/runtime/ITERATION_LOG.md`
- Current artifact behavior:
  - This skill writes its active iteration log under the runtime root.
  - This skill does not emit file artifacts under the result root yet.
  - Any future targeted artifact command must accept an explicit output path or default under the governed result root.

## Example Commands
- Load working contract:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/skill-production-form && python3 scripts/Cli_Toolbox.py working-contract --json | sed -n '1,200p'`
- Load current intent snapshot:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/skill-production-form && python3 scripts/Cli_Toolbox.py intent-snapshot --json | sed -n '1,200p'`
- Load latest log:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/skill-production-form && python3 scripts/Cli_Toolbox.py latest-log --json | sed -n '1,200p'`
- Append a new local design log entry:
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/skill-production-form && python3 scripts/Cli_Toolbox.py append-iteration-log --title "Refine console boundary" --summary "Locked the Skills directory as the console productization source surface." --decision "Keep runtime contracts and registry aligned with the skill root" --affected-path "skill-production-form/SKILL.md" --next-step "Continue consolidating console-facing skill governance" --json | sed -n '1,200p'`
