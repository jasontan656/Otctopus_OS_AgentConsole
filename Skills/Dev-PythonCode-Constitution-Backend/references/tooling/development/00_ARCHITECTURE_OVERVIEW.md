---
doc_id: "dev_pythoncode_constitution_backend.tooling.architecture_overview"
doc_type: "topic_atom"
topic: "Tooling architecture overview for the Python backend code constitution skill"
anchors:
  - target: "../Cli_Toolbox_DEVELOPMENT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The tooling development entry routes readers into this overview."
  - target: "../../governance/SKILL_EXECUTION_RULES.md"
    relation: "pairs_with"
    direction: "downstream"
    reason: "Any future tooling must stay aligned with the execution rules."
---

# Cli_Toolbox 开发文档架构总览

适用技能：`Dev-PythonCode-Constitution-Backend`

## 目标
- 记录本技能当前 Python lint 工具链的结构与边界，并为未来的 Python 代码治理扩展保留结构化入口。

## 分层结构
1. 入口层：`references/tooling/Cli_Toolbox_DEVELOPMENT.md`
2. 索引层：`10_MODULE_CATALOG.yaml`、`20_CATEGORY_INDEX.md`
3. 模块层：`references/tooling/development/modules/`
4. 变更层：`90_CHANGELOG.md`

## 额外要求
- 当前技能的真实执行面由“文档树 + Python lint CLI”共同组成。
- `run_python_code_lints.py` 只负责 Python 代码治理，不承接宪法查询。
- 若未来新增工具，必须明确它只负责辅助读取、校验或生成，不得绕过 `SKILL.md -> TASK_ROUTING -> governance atom -> python_rules` 的主路径。
