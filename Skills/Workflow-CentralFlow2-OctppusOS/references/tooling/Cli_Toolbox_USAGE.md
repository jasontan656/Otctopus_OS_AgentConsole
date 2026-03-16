---
doc_id: workflow_centralflow2_octppusos.references.tooling.cli_toolbox_usage
doc_type: topic_atom
topic: CLI usage for Workflow-CentralFlow2-OctppusOS
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This file documents the governed CLI usage surface.
---

# Cli_Toolbox Usage

## Contract First
```bash
python3 ./scripts/Cli_Toolbox.py contract --json
python3 ./scripts/Cli_Toolbox.py read-contract-context --entry development_loop --json
```

## Runtime Resolution
```bash
python3 ./scripts/Cli_Toolbox.py target-runtime-contract --target-root <repo> --docs-root <docs_root> --json
python3 ./scripts/Cli_Toolbox.py stage-checklist --stage mother_doc --target-root <repo> --docs-root <docs_root> --json
```

## State-Changing Commands
```bash
python3 ./scripts/Cli_Toolbox.py target-scaffold --target-root <repo> --docs-root <docs_root> --json
python3 ./scripts/Cli_Toolbox.py mother-doc-audit --path <mother_doc_root> --json
python3 ./scripts/Cli_Toolbox.py construction-plan-init --target <pack_root> --plan-kind official_plan --json
python3 ./scripts/Cli_Toolbox.py acceptance-lint --matrix-path <matrix> --report-path <report> --json
```

## Notes
- Prefer `contract --json` over `runtime-contract --json`.
- The deeper workflow rationale remains in `path/development_loop/supporting/SKILL_TOOLING_EXECUTION_PLAYBOOK.md`.
