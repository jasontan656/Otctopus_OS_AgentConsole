---
doc_id: skillsmanager_tooling_checkup.references.policies.contract_audit_policy
doc_type: topic_atom
topic: Contract audit policy
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This policy defines the minimum runtime contract requirements.
---

# Contract Audit Policy

## 最小要求
- scripted skill 至少应提供：
  - `skill_name`
  - `tool_entry`
  - `runtime_source_policy`
- 若 target skill 具备显式 profile，则 contract 中应反映 profile 或 profile support。
- 审计优先级：
  1. `references/runtime_contracts/SKILL_RUNTIME_CONTRACT.json`
  2. `Cli_Toolbox.py contract --json`

## 禁止事项
- 不要把命令名本身当长期标准。
- 不要因为 target 有 `path/` 就假定它必须有某个旧 family 命令。
