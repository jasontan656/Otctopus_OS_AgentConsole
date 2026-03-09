# Target Rule Audit

> Human audit copy generated from the skill-managed target runtime JSON.
> Runtime models must call the listed CLI instead of reading this markdown.

## Target
- relative_path: `octopus_os_root`
- scope_branch: `octopus_os_root`
- file_kind: `agents`
- source_path: `/home/jasontan656/AI_Projects/Octopus_OS/AGENTS.md`

## Runtime Entry
- cli: `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack/scripts/Cli_Toolbox.py mother-doc-agents-target-contract --relative-path "octopus_os_root" --file-kind agents --json`
- runtime_json_path: `/home/jasontan656/AI_Projects/Codex_Skills_Mirror/2-Octupos-FullStack/assets/mother_doc_agents/runtime_rules/octopus_os_root/AGENTS.runtime.json`

## Peer Doc
- path: `/home/jasontan656/AI_Projects/Octopus_OS/README.md`
- read_policy: `optional_then_required_on_write_if_exists`

## Turn Contract
- status: `enforced`
- turn_start:
  - if the turn will write Octopus_OS, plan same-turn Constitution lint from the start
  - use the returned target contract JSON as the runtime rule source
- turn_end:
  - if the turn wrote Octopus_OS, run Constitution lint on the concrete target root
