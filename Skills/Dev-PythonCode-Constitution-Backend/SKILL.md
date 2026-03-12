---
name: "Dev-PythonCode-Constitution-Backend"
description: "关于 Python 代码的规范和指引。"
metadata:
  doc_structure:
    doc_id: "dev_pythoncode_constitution_backend.entry.facade"
    doc_type: "skill_facade"
    topic: "Entry facade for the Python backend code constitution skill"
    anchors:
      - target: "references/routing/TASK_ROUTING.md"
        relation: "routes_to"
        direction: "downstream"
        reason: "The facade must route readers into the first task branch."
      - target: "references/governance/SKILL_DOCSTRUCTURE_POLICY.md"
        relation: "governed_by"
        direction: "downstream"
        reason: "Doc-structure policy is a mandatory governance branch."
---

# Dev-PythonCode-Constitution-Backend

## 1. 技能定位
- 本文件只做门面入口，不承载深规则正文。
- 本技能用于收敛“关于 Python 代码的规范和指引”这一单一主轴，默认面向后端代码语境。
- 当前职责已经扩展为两类且仅两类：Python 代码规范/拆分指引，以及 Python 相关静态 lint。
- 从 `Constitution-knowledge-base` 迁出的胖代码检查、拆分指引与 Python 专属 lint 工具，统一由本技能接管。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务涉及胖代码阈值、拆分落点，再读取 `references/python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`。
5. 若任务涉及 typing、data boundary、concurrency、import side effect、exception、logging、subprocess、HTTP timeout 或 Python 工程安全边界，再读取 `references/python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`。
6. 若任务涉及 pytest、package resource、`pyproject.toml`、entrypoint 或 Python 项目集成边界，再读取 `references/python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`。
7. 若任务涉及 lint 执行或工具维护，再进入 `references/tooling/`。

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- Python 规则层：
  - `references/python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`
  - `references/python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`
  - `references/python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`
- 工具层：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/Cli_Toolbox_DEVELOPMENT.md`

## 4. 适用域
- 适用于：Python 代码规范判定、Python 代码写作指引、Python 代码审查与改写、胖代码阈值检查、固定拆分落点治理、Python 相关静态 lint。
- 不适用于：前端规范、非 Python 语言规范、未提供证据时对框架或项目私有约定的臆测。
- 若任务需要第三方框架、库或工具链的实时规则，应以当时官方文档或用户补充为准，本技能不内置时效性结论。

## 5. 执行入口
- 规则读取入口：`SKILL.md -> references/routing/TASK_ROUTING.md -> references/governance/SKILL_EXECUTION_RULES.md`
- Python 胖代码/拆分规则入口：`references/python_rules/PYTHON_FAT_FILE_CONSTITUTION.md`
- lint 执行入口：`./.venv_backend_skills/bin/python Skills/Dev-PythonCode-Constitution-Backend/scripts/run_python_code_lints.py --target <target_root>`
- 若后续新增或改写工具，必须同步更新 `references/tooling/` 全套文档。

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 未提供的信息默认保持未知，不把常见 Python 风格偏好写成本技能既定规则。

## 7. 结构索引
```text
Dev-PythonCode-Constitution-Backend/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── run_python_code_lints.py
│   └── python_code_lint_rules/
├── references/
│   ├── governance/
│   ├── python_rules/
│   ├── routing/
│   ├── runtime/        # optional
│   └── tooling/
├── assets/
└── tests/
```
