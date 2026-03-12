---
doc_id: "dev_pythoncode_constitution_backend.routing.task_routing"
doc_type: "routing_doc"
topic: "Route readers by Python code task intent"
anchors:
  - target: "../../SKILL.md"
    relation: "implements"
    direction: "upstream"
    reason: "This routing doc is the first branch below the skill facade."
  - target: "../governance/SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Skill maintenance and structure changes must pass through doc-structure policy."
  - target: "../governance/SKILL_EXECUTION_RULES.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Python code queries and review tasks should enter the execution rules doc."
---

# Task Routing

## 当前分叉轴线
- 本文只按“Python 代码相关任务意图”分流，不承载具体规范条文。

## 分支一：查询或对齐 Python 代码规范
- 先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 若任务明确落到胖代码阈值、固定拆分落点或 Python 文件职责模板，再读 `../python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`。
- 若任务明确落到 typing、data boundary、concurrency、import side effect、exception、logging、subprocess、HTTP timeout 或 Python 工程安全边界，再读 `../python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`。
- 若任务明确落到 pytest、package resource、`pyproject.toml`、entrypoint 或 Python 项目集成边界，再读 `../python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`。
- 若规范来源来自用户输入、仓内现有代码或外部官方文档，再以这些证据为准继续收敛。

## 分支二：运行 Python 相关静态 lint
- 先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 再读 `../python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`，确认当前 lint 的治理依据。
- 若 lint 涉及 typing、data boundary、concurrency、import side effect、exception、logging、subprocess、HTTP timeout 安全边界，也要同时读 `../python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`。
- 若 lint 涉及 pytest、package resource、`pyproject.toml` 或 entrypoint，也要同时读 `../python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`。
- 然后执行 `./.venv_backend_skills/bin/python Skills/Dev-PythonCode-Constitution-Backend/scripts/run_python_code_lints.py --target <target_root>`。

## 分支三：维护本技能自身结构
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`。
- 若未来新增或修改专属工具，再进入 `../tooling/Cli_Toolbox_USAGE.md` 与 `../tooling/Cli_Toolbox_DEVELOPMENT.md`。
