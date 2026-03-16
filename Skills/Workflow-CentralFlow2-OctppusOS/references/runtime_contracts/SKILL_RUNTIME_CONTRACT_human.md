---
doc_id: workflow_centralflow2_octppusos.references.runtime_contracts.skill_runtime_contract_human
doc_type: topic_atom
topic: Human mirror of the Workflow-CentralFlow2-OctppusOS runtime contract
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document mirrors the governed runtime contract for humans.
---

# Workflow-CentralFlow2-OctppusOS Runtime Contract

## Primary Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py contract --json`
- Context compiler entry: `./.venv_backend_skills/bin/python Skills/Workflow-CentralFlow2-OctppusOS/scripts/Cli_Toolbox.py read-contract-context --entry development_loop --json`
- `runtime-contract` is retained only as a compatibility alias.

## Profile
- `doc_topology`: `workflow_path`
- `tooling_surface`: `automation_cli`
- `workflow_control`: `compiled`

## Contract Notes
- Machine truth lives in `SKILL_RUNTIME_CONTRACT.json`.
- Runtime writes are resolved through `target-runtime-contract`; this skill does not own a private artifact root.
- Tooling usage and maintenance notes are governed under `references/tooling/`.
