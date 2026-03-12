---
doc_id: "dev_pythoncode_constitution_backend.python_rules.runtime_safety"
doc_type: "topic_atom"
topic: "Python runtime safety and engineering governance"
anchors:
  - target: "../governance/SKILL_EXECUTION_RULES.md"
    relation: "implements"
    direction: "upstream"
    reason: "The execution rules route typing, logging, and subprocess topics here."
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends runtime-safety and engineering-governance tasks here."
---

# Python Runtime Safety Constitution

## 在项目中起什么作用
- 为 Python 工程中的类型边界、子进程调用边界、日志边界提供明确可执行的治理规则。
- 把“建议”收敛为可被 lint 自动检查的硬规则，避免在 review 阶段反复口头提醒。
- 与胖文件治理互补：胖文件解决结构膨胀，本文件解决运行时安全与工程契约失真。

## 适用范围
- 适用于：`.py` 文件本体。
- 适用于：Python CLI、backend service、tooling script、worker、adapter、orchestrator。
- 不适用于：纯文档、前端文件、未被确认属于 Python 资产的非 `.py` 文件。

## 当前强制规则

### 1. Typing Governance
1. 公共函数必须补齐参数与返回值类型注解。
2. 公共函数签名中默认禁止使用无约束的 `Any`。
3. `self` 与 `cls` 可不显式标注。
4. 私有函数（以下划线开头）可暂不进入此条强制门禁，但推荐继续补齐。

### 2. Subprocess Safety
1. 默认优先使用 `subprocess.run(...)`，不要把简单命令执行退化为 `Popen(...)`。
2. 默认禁止 `shell=True`。
3. 若确实需要 `Popen(...)`，必须能说明原因，例如流式交互或增量 IO；不要把它当成默认入口。

### 3. Logging Boundary
1. library-style Python 模块必须使用命名 logger，例如 `logging.getLogger(__name__)`。
2. 非 CLI 入口文件禁止直接调用 root logger，如 `logging.info(...)`、`logging.error(...)`。
3. 非 CLI 入口文件禁止调用 `logging.basicConfig(...)`。
4. `logging.getLogger()` 不得省略名字或传空字符串。

## 当前 lint gate 映射

| gate | 负责内容 |
|---|---|
| `typing_governance_gate` | 公共函数缺失注解、公共签名使用 `Any` |
| `subprocess_safety_gate` | `Popen(...)` 默认滥用、`shell=True` |
| `logging_boundary_gate` | root logger、`basicConfig(...)`、匿名 logger |

## 设计依据
1. PEP 484 与 mypy existing-code 指南支持逐步收紧公共 API 的类型边界，降低改动扩散时的隐式破坏。
2. Python 官方 `subprocess` 文档建议优先使用高层 `run()` API，并强调 shell 调用的安全边界。
3. Python Logging HOWTO 明确区分 library code 与 application bootstrap：库代码应使用命名 logger，而不是配置 root logger。

## 必须做（Do）
1. 为公共函数补齐参数和返回值注解。
2. 在 Python 代码中优先传 `argv list` 给 `subprocess.run(...)`。
3. 在模块级创建 `logger = logging.getLogger(__name__)`，由命名 logger 负责输出。
4. 把 logging 配置集中到真正的 CLI 或应用启动层。

## 不要做（Don't）
1. 不要在公共函数签名中随手写 `Any` 作为兜底。
2. 不要把 `Popen(...)` 当成普通命令执行的默认模板。
3. 不要用 `shell=True` 作为快捷方式。
4. 不要在 library-style 模块里直接 `logging.info(...)` 或 `logging.basicConfig(...)`。

## 最小验收
1. 新增与修改的公共函数具备完整类型注解。
2. 默认 Python 命令执行使用 `subprocess.run(...)`，且没有 `shell=True`。
3. 非 CLI 模块全部使用命名 logger，且不修改 root logging 配置。
4. 违反以上规则时，`python3 scripts/run_python_code_lints.py --target <target_root>` 返回非零退出码。
