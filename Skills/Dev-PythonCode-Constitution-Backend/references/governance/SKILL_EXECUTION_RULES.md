---
doc_id: "dev_pythoncode_constitution_backend.governance.execution_rules"
doc_type: "topic_atom"
topic: "Execution rules for Python code guidance and review"
anchors:
  - target: "SKILL_DOCSTRUCTURE_POLICY.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Execution rules and structure policy must evolve together."
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Python code tasks enter the skill through this execution-rules doc."
---

# Skill Execution Rules

## 本地目的
- 为“关于 Python 代码的规范和指引”相关任务提供执行边界、证据优先级、未知处理规则，以及 Python 专属 lint 的使用门禁。

## 当前边界
- 本文不直接发明具体的 Python 风格条文，不替代用户、项目或官方文档已经存在的规则源。
- 本文只定义如何判断哪些规则可用、哪些信息仍然未知，以及什么时候应触发 `run_python_code_lints.py`。

## 局部规则
- 先判断当前任务是否确实属于 Python 代码范围；若不是，本技能不应被当成默认规则源。
- 规则来源优先级依次为：用户明确给出的规范、仓内已存在的稳定模式、官方文档或主源资料、最后才是通用工程判断。
- 当用户未提供框架、版本、项目约定或风格基线时，必须显式标记“未知”，不得把常见偏好伪装成既定规范。
- 对代码审查、改写或生成请求，应说明建议依据来自哪里；若依据不足，应先收缩结论而不是扩张规范。
- 涉及第三方库、框架、lint、typing、测试工具等时效性规则时，应以当时官方文档为准，本技能不缓存实时真相。
- 若任务内容包含 Python 相关编辑，且需要在回合末执行结构/边界校验，应运行 `python3 scripts/run_python_code_lints.py --target <target_root>`。
- 运行 lint 前，先确认目标范围与 Python 相关；不要把非 Python 任务或纯文档任务强行套进本技能的 lint 链路。
- lint 的治理对象只包括两类：`.py` 文件本体，以及已被 Python 文件引用或在内容/路径上具备明确 Python 证据的非 `.py` 资产。
- 仅因文件名包含 `contract`、`rule`、`rules`、`constitution`、`lint`，不足以判定该文件受本技能治理；必须先确认它属于 Python 资产或 Python 语境。
- 通用目录命名、泛文件结构整治这类与 Python 语义无直接关系的规则，不应继续挂在本技能 lint 下。
- 若任务涉及 typing、exception、logging、subprocess、HTTP timeout 或 Python 运行时安全边界，应同步读取 `../python_rules/PYTHON_RUNTIME_SAFETY_CONSTITUTION.md`。
- 当前 lint 还负责五类 Python 工程安全规则：公共函数类型注解边界、异常治理边界、`subprocess` 调用安全边界、HTTP timeout 边界、`logging` 命名 logger 边界。
- 若任务涉及 pytest、package resource、`pyproject.toml` 或 CLI entrypoint 集成边界，应同步读取 `../python_rules/PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md`。
- 当前 lint 还负责三类 Python 项目集成规则：pytest importlib/strict markers、package resource loading、`pyproject.toml` packaging metadata 与 `project.scripts`。
- 对胖文件问题，必须同时给出“为什么超限”与“应该拆到哪里”；不能只报告行数，不给固定拆分落点。

## 例外与门禁
- 若任务要求的是具体业务实现而不是代码规范/指引，应退出本技能主轴，转入对应业务技能或代码上下文。
- 若当前仓库已有更强的 repo-local 合同、现成 lint 规则或 framework 规范，这些规则优先于本技能的通用执行边界。
- 若目标目录中没有 Python 相关修改内容，本技能的 lint 可不触发。
