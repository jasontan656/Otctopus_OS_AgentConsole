---
doc_id: "dev_pythoncode_constitution_backend.tooling.changelog"
doc_type: "topic_atom"
topic: "Tooling changelog for the Python backend code constitution skill"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The changelog belongs to the tooling development doc set."
  - target: "../../governance/SKILL_EXECUTION_RULES.md"
    relation: "tracks_changes_to"
    direction: "downstream"
    reason: "Tooling changes may affect execution rules."
---

# Cli_Toolbox 开发文档变更记录

- 2026-03-12
  - 创建 `Dev-PythonCode-Constitution-Backend` basic 技能骨架。
  - 迁入 `run_python_code_lints.py` 与 `python_code_lint_rules/`。
  - 接管 Python 胖代码治理与拆分指引，不再由 `Constitution-knowledge-base` 承担。
