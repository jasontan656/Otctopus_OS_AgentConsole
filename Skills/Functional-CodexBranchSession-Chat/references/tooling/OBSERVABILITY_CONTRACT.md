# Observability Contract


## Contract Header
- `contract_name`: `functional_codex_branch_session_chat_references_tooling_observability_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

## Runtime Anchors
- `Codex_Skill_Runtime/Functional-CodexBranchSession-Chat/machine.jsonl`
- `Codex_Skill_Runtime/Functional-CodexBranchSession-Chat/human.log`
- `logs/machine.jsonl`（project-local anchor）
- `logs/human.log`（project-local anchor）

## Channel Semantics
- `machine.jsonl`: structured machine events for replay and automation checks.
- `human.log`: readable execution timeline for operator diagnosis.

## Minimal Event Fields
- `run_id`
- `audit_trace`
- `session_id`
- `status`
