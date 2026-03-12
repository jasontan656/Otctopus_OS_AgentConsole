---
doc_id: "dev_pythoncode_constitution_backend.tooling.toolbox_usage"
doc_type: "topic_atom"
topic: "Tooling usage status for the Python backend code constitution skill"
anchors:
  - target: "Cli_Toolbox_DEVELOPMENT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Usage and development status should be updated together."
  - target: "../governance/SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "Tooling docs remain part of the governed doc tree."
---

# Cli_Toolbox 使用文档

适用技能：`Dev-PythonCode-Constitution-Backend`

## 当前状态
- 当前不提供统一 `Cli_Toolbox.py`，但已经提供 Python 专属 lint CLI：`scripts/run_python_code_lints.py`。
- 当前技能的工具面只负责 Python 代码治理，不承接宪法查询。

## 最小使用方式
- 进入 `SKILL.md`，再按 `references/routing/TASK_ROUTING.md` 进入具体分支。
- 查询、审查或改写 Python 代码时，固定读取 `references/governance/SKILL_EXECUTION_RULES.md` 与 `references/python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`。
- 需要执行静态校验时，运行 `python3 scripts/run_python_code_lints.py --target <target_root>`。

## 命令约束
- 一行命令：
  - `cd /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Dev-PythonCode-Constitution-Backend && python3 scripts/run_python_code_lints.py --target /home/jasontan656/AI_Projects/octopus-os-agent-console/Skills/Dev-PythonCode-Constitution-Backend | cat`
- 当前 CLI 只接受 `--target`。
- lint 输出为单个 JSON 对象；任一 gate 失败时返回非零退出码。
- lint 会显式排除虚拟环境、构建产物、缓存与临时目录，例如 `.venv*`、`venv*`、`node_modules/`、`dist/`、`build/`、`coverage/`、`tmp/`、`temp/`、`.tmp*`、`.temp*`、`__pycache__/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/`。
- lint 默认只扫描 `.py` 文件与已确认属于 Python 资产的非 `.py` 文件；未被 Python 引用、且没有明确 Python 语境的 `contract` / `rules` / `policy` 文档不会被纳入治理。
- 通用目录命名与泛文件结构检查已退出该 CLI，不再作为 Python lint 的默认职责。

## 同步维护要求
- 修改工具行为后，必须同步更新本文件与 `Cli_Toolbox_DEVELOPMENT.md`。
- 若未来新增更多 Python 代码治理 CLI，还必须同步更新 `references/tooling/development/` 下的目录与模块文档。
