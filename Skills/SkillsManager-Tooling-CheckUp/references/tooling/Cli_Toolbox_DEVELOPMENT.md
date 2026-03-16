---
doc_id: skillsmanager_tooling_checkup.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: Development notes for SkillsManager-Tooling-CheckUp tooling
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool development notes must stay synchronized with the implementation.
---

# Cli_Toolbox Development

## 模块边界
- `audit_models.py`
  - typed audit issue/result data
- `contract_validator.py`
  - runtime contract loading and field validation
- `runtime_probe.py`
  - CLI/tests/tooling doc surface detection
- `artifact_audit.py`
  - artifact policy inspection
- `remediation_gate.py`
  - next-step remediation assembly
- `audit_orchestrator.py`
  - assemble final audit payload
- `Cli_Toolbox.py`
  - thin dispatcher

## 同步要求
- 改 contract schema、artifact policy rules、audit payload 或 CLI 参数时，必须同步更新：
  - `references/runtime_contracts/`
  - `references/policies/`
  - `references/tooling/`
  - `tests/`
