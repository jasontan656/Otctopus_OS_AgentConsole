# Tool Doc Sync Contract

## Scope
- managed_skill: `2-Task-runtime-selfcheck`
- applies_to: all tools in runtime registry and toolbox scripts

## Mandatory Rules
- Any self-evolution change must keep script, runtime registry, and structured docs synchronized.
- `runtime/TOOL_DOCS_STRUCTURED.yaml` and `runtime/TOOL_REGISTRY.yaml` must stay tool_id-aligned.
- Machine-map anchors must be updated when script paths, docs paths, or evidence paths change.
- Every material tool evolution must append one traceable entry to `runtime/TOOL_CHANGE_LEDGER.jsonl`.

## Required Verification
- Run `mstg_l0_l13_full_gate_lint.py` and require PASS.
- Run `mstg_target_governance_outcome_lint.py` and require PASS.
- Confirm outcome lint has zero high-severity violations before release.
