[AGENT RUNTIME HOOK - ABSOLUTE ENFORCEMENT]

`HOOK_LOAD`: Apply this AGENTS contract. This file is a thin runtime entry that points to the skill-managed CLI/JSON rule source.

[TURN START - MANDATORY]

1. Load Target Contract
- Must run this command before following any path-specific rule:
- `python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md" --json`

2. TURN_START Contract
- N/A

3. Peer Document Gate
- See the returned `peer_doc` object to decide whether the same-level peer file exists and whether it must be read.

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

[PART B]
```json
{
  "schema_version": 1,
  "owner_skill": "Meta-Default-md-manager",
  "managed_branch": "default_docs",
  "rule_source_policy": {
    "runtime_rule_source": "CLI_JSON",
    "human_audit_source": "audit_markdown_only",
    "model_must_not_read_markdown_for_runtime_guidance": true
  },
  "target": {
    "source_root": "/home/jasontan656/AI_Projects",
    "source_path": "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md",
    "source_relative_path": "Octopus_CodeBase_Frontend/AGENTS.md",
    "file_kind": "agents",
    "target_kind": "AGENTS.md",
    "peer_path": "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/README.md",
    "managed_rel_path": "AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md",
    "managed_dir": "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Octopus_CodeBase_Frontend",
    "human_path": "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Octopus_CodeBase_Frontend/AGENTS_human.md",
    "machine_path": "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Octopus_CodeBase_Frontend/AGENTS_machine.json"
  },
  "peer_doc": {
    "path": "/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/README.md",
    "relation": "same_level_summary",
    "read_policy": "optional_then_required_on_write_if_exists"
  },
  "runtime_entry": {
    "cli": "python3 /home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/scripts/Cli_Toolbox.py target-contract --source-path \"/home/jasontan656/AI_Projects/Octopus_CodeBase_Frontend/AGENTS.md\" --json",
    "audit_md_path": "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Octopus_CodeBase_Frontend/AGENTS_human.md",
    "runtime_json_path": "/home/jasontan656/AI_Projects/Codex_Skills_Mirror/Meta-Default-md-manager/assets/managed_targets/AI_Projects/Octopus_CodeBase_Frontend/AGENTS_machine.json"
  },
  "turn_contract": {
    "status": "n_a",
    "turn_start": [
      "N/A"
    ],
    "turn_end": [
      "N/A"
    ]
  },
  "routing": {
    "document_role": "runtime_entry",
    "default_next_hop": "use the target-contract JSON to decide peer reads and manager commands",
    "rules": [
      "use Meta-Default-md-manager CLI JSON as the runtime rule source",
      "README-like files remain human summaries unless a peer AGENTS contract says otherwise",
      "machine-readable runtime rules must stay in skill-managed JSON and CLI output"
    ]
  },
  "update_boundary": [
    "managed targets are owned by Meta-Default-md-manager",
    "external AGENTS.md should remain a thin runtime entry",
    "skill-managed JSON and CLI output are the runtime source of truth"
  ]
}
```
