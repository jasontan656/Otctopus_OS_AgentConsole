---
doc_id: skillsmanager_doc_structure.references.tooling.cli_toolbox_development
doc_type: topic_atom
topic: Development notes for SkillsManager-Doc-Structure tooling
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: Tool development notes must stay synchronized with the implementation.
---

# Cli_Toolbox Development

## 模块边界
- `doc_models.py`
  - typed report data and profile summary
- `profile_detector.py`
  - topology detection
- `facade_linter.py`
  - facade section and metadata checks
- `reference_graph.py`
  - referenced layout checks
- `workflow_compiler.py`
  - context compilation and workflow edge checks
- `audit_orchestrator.py`
  - assemble inspect/lint payloads
- `Cli_Toolbox.py`
  - argument parsing and command dispatch

## 同步要求
- 改 CLI 参数、report payload、profile detection 或 lint scope 时，必须同步更新：
  - `references/runtime_contracts/`
  - `references/policies/`
  - `references/tooling/`
  - `tests/`
