---
doc_id: dev_pythoncode_constitution.tooling.changelog
doc_type: topic_atom
topic: Tooling changelog for the Python code constitution skill
anchors:
- target: ../Cli_Toolbox_DEVELOPMENT.md
  relation: implements
  direction: upstream
  reason: The changelog belongs to the tooling development doc set.
- target: ../../governance/SKILL_EXECUTION_RULES.md
  relation: tracks_changes_to
  direction: downstream
  reason: Tooling changes may affect execution rules.
---

# Cli_Toolbox 开发文档变更记录

- 2026-03-12
  - 创建 `Dev-PythonCode-Constitution` basic 技能骨架。
  - 迁入 `run_python_code_lints.py` 与 `python_code_lint_rules/`。
  - 接管 Python 胖代码治理与拆分指引。
  - 收紧 lint 治理边界：非 `.py` 文件需先确认属于 Python 资产，不能仅凭 `contract` / `rules` 命名纳管。
  - 移除 runner 中的泛目录结构 gate，避免越界治理非 Python 文件结构。
  - 新增 `typing_governance_gate`、`subprocess_safety_gate`、`logging_boundary_gate`，把 Python runtime safety 纳入技能治理面。
  - 新增 `references/python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`，承载 typing / subprocess / logging 原子规则。
  - 新增 `pytest_governance_gate`、`resource_loading_gate`、`packaging_entrypoint_gate`，把 Python 项目集成治理纳入技能治理面。
  - 新增 `references/python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`，承载 pytest / resource / packaging 原子规则。
  - 新增 `exception_governance_gate` 与 `http_timeout_gate`，把异常治理与外部 HTTP 超时边界纳入 runtime safety。
  - 新增 `data_boundary_gate` 与 `concurrency_boundary_gate`，把 payload/data contract 与并发生命周期边界纳入 runtime safety。
  - 调整 runtime safety 边界：移除越界的 `io_boundary_gate` 与 `time_random_boundary_gate`，仅保留 `import_side_effect_gate` 作为 Python 通用实践治理。
