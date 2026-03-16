---
doc_id: workflow_centralflow2_octppusos.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: CLI development notes for Workflow-CentralFlow2-OctppusOS
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This file documents the governed CLI maintenance surface.
---

# Cli_Toolbox Development

## Module Split
- `scripts/Cli_Toolbox.py`: thin executable entrypoint only.
- `scripts/cli_parser.py`: argparse tree and subcommand registration.
- `scripts/cli_commands.py`: command handlers and runtime guards.
- `scripts/workflow_centralflow2_runtime.py`: contract loading and markdown-chain compilation.

## Maintenance Rules
- Keep `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json` synchronized with the payload returned by `contract --json`.
- Keep new CLI commands documented here and surfaced through `tool_entry.commands`.
- Keep regression coverage under `tests/`; `scripts/test_cli_toolbox.py` is no longer the authoritative test suite.
- When changing workflow semantics, update stage contract markdown and the stage-specific Python payloads in the same turn.
