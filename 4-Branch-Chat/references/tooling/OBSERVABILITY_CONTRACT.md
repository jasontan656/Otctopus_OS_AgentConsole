# Observability Contract

## Runtime Anchors
- `Codex_Skill_Runtime/4-Branch-Chat/machine.jsonl`
- `Codex_Skill_Runtime/4-Branch-Chat/human.log`
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
