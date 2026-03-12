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
- 为 Python 工程中的类型边界、data contract 边界、并发生命周期边界、I/O 副作用边界、时间/随机性边界、import 时副作用边界、异常边界、子进程调用边界、HTTP 超时边界、日志边界提供明确可执行的治理规则。
- 把“建议”收敛为可被 lint 自动检查的硬规则，避免在 review 阶段反复口头提醒。
- 与胖文件治理互补：胖文件解决结构膨胀，本文件解决运行时安全与工程契约失真。
- pytest、package resource、`pyproject.toml`、entrypoint 等项目集成边界由配套文档 `PYTHON_PROJECT_INTEGRATION_CONSTITUTION.md` 承担，不在本文件混写。

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

### 2. Data Boundary
1. 公共 payload-like 接口参数默认禁止直接暴露原始 `dict` / `Mapping` / `MutableMapping` 合同。
2. 对 `payload`、`body`、`event`、`message`、`update`、`record`、`envelope` 这类参数名，优先使用 `TypedDict`、dataclass 或明确模型类型。
3. 名称语义明确属于 payload-like 的公共返回值，也不应再用原始 `dict` / `Mapping` 作为最终合同。

### 3. Concurrency Boundary
1. 默认禁止把 `asyncio.create_task(...)` 作为孤儿 fire-and-forget 调用直接丢弃。
2. `create_task(...)` 产生的 task 句柄必须被保存、返回、await，或交给 `TaskGroup` 等更明确的拥有者。
3. `ThreadPoolExecutor` / `ProcessPoolExecutor` 默认要求放在 `with ... as executor:` 中管理生命周期。

### 4. Exception Governance
1. 默认禁止裸 `except:`。
2. 默认禁止捕获 `BaseException`。
3. 捕获广义 `Exception` 时，默认要求继续 `raise`；不要静默吞掉真实错误边界。

### 4. IO Boundary
1. 命名或路径语义上属于 pure/core layer 的文件，不应直接执行网络、文件、socket 或 subprocess I/O。
2. `domain`、`entity`、`model`、`policy`、`value object` 这类边界应只消费数据，不直接创建 HTTP client/session 或直接读写文件。
3. 真实副作用应下沉到 adapter、gateway、repository、CLI/bootstrap 边界。

### 5. Time And Random Boundary
1. core logic 文件默认不应直接调用 `datetime.now()`、`date.today()`、`time.time()`。
2. core logic 文件默认不应直接调用 `uuid.uuid4()` 或 `random.*` 生成不稳定输入。
3. 时间、ID 与随机性应来自显式 `clock`、`id_provider`、`rng` 边界。

### 6. Import Side Effect Boundary
1. import 模块时默认不应直接发起 I/O、创建 runtime client、构造 executor、启动 background task。
2. import 模块时默认不应生成当前时间、随机值或 UUID 作为运行态状态。
3. 这类动作应放进显式函数、factory、startup hook 或 `__main__` guard。

### 7. Exception Governance
1. 默认禁止裸 `except:`。
2. 默认禁止捕获 `BaseException`。
3. 捕获广义 `Exception` 时，默认要求继续 `raise`；不要静默吞掉真实错误边界。

### 8. Subprocess Safety
1. 默认优先使用 `subprocess.run(...)`，不要把简单命令执行退化为 `Popen(...)`。
2. 默认禁止 `shell=True`。
3. 若确实需要 `Popen(...)`，必须能说明原因，例如流式交互或增量 IO；不要把它当成默认入口。

### 9. HTTP Timeout Boundary
1. 使用 `requests` 发起 HTTP 请求时，必须显式声明 `timeout=`。
2. `requests` 中默认禁止 `timeout=None`。
3. `httpx` 已有默认超时，因此默认禁止显式写 `timeout=None` 来关闭超时。

### 10. Logging Boundary
1. library-style Python 模块必须使用命名 logger，例如 `logging.getLogger(__name__)`。
2. 非 CLI 入口文件禁止直接调用 root logger，如 `logging.info(...)`、`logging.error(...)`。
3. 非 CLI 入口文件禁止调用 `logging.basicConfig(...)`。
4. `logging.getLogger()` 不得省略名字或传空字符串。

## 当前 lint gate 映射

| gate | 负责内容 |
|---|---|
| `typing_governance_gate` | 公共函数缺失注解、公共签名使用 `Any` |
| `data_boundary_gate` | payload-like 公共接口禁止原始 `dict` / `Mapping` 合同 |
| `concurrency_boundary_gate` | 孤儿 `asyncio.create_task(...)`、未受 `with` 管理的 executor |
| `io_boundary_gate` | pure/core layer 禁止直接网络、文件、socket、subprocess I/O |
| `time_random_boundary_gate` | core logic 中禁止直接读取时间、UUID、随机性 |
| `import_side_effect_gate` | 模块 import 时禁止直接做 I/O、runtime 初始化、时间/随机值生成 |
| `exception_governance_gate` | 裸 `except`、`BaseException`、广义异常静默吞掉 |
| `subprocess_safety_gate` | `Popen(...)` 默认滥用、`shell=True` |
| `http_timeout_gate` | `requests` 缺少 timeout、`timeout=None` 禁用超时 |
| `logging_boundary_gate` | root logger、`basicConfig(...)`、匿名 logger |

## 设计依据
1. PEP 484 与 mypy existing-code 指南支持逐步收紧公共 API 的类型边界，降低改动扩散时的隐式破坏。
2. Python 官方 `typing.TypedDict` 与 `dataclasses` 文档都强调为结构化数据提供显式可检查的契约，而不是让匿名 `dict` 漫游跨边界。
3. Python 官方 `asyncio.create_task` 文档要求保存 task 引用，`concurrent.futures` 文档也将 executor 的上下文管理作为标准生命周期写法。
4. Python 官方 import system 文档明确说明模块在首次导入时会执行模块代码，因此 import-time I/O、client 初始化与时间/随机值生成会把运行态副作用偷偷绑在加载阶段。
5. Python 官方 `datetime`、`time`、`uuid`、`random` 文档都说明这些 API 会读取当前时间或生成新的不稳定值，因此更适合作为显式 runtime provider，而不是 core logic 的隐式依赖。
6. Python 官方 errors/exceptions 教程要求异常处理尽可能具体，并强调意外异常应继续传播。
7. Python 官方 `subprocess` 文档建议优先使用高层 `run()` API，并强调 shell 调用的安全边界。
8. Requests 官方文档说明默认不会超时，生产侧请求应显式设置 `timeout`；HTTPX 官方文档说明默认有超时，但 `timeout=None` 会关闭它。
9. Python Logging HOWTO 明确区分 library code 与 application bootstrap：库代码应使用命名 logger，而不是配置 root logger。

## 必须做（Do）
1. 为公共函数补齐参数和返回值注解。
2. 对 payload-like 入参与返回值使用 `TypedDict`、dataclass 或明确模型类型。
3. 保存或显式归属 `asyncio.create_task(...)` 返回的 task，并用 `with` 管理 executor 生命周期。
4. 把网络、文件、socket、subprocess 这类真实 I/O 下沉到 adapter、gateway、repository 或 startup 边界。
5. 让 core logic 通过 `clock`、`id_provider`、`rng` 等显式依赖拿到不稳定输入。
6. 保持模块 import 轻量且确定，把 runtime 初始化延后到显式函数或启动阶段。
7. 对意外异常保持明确边界，捕获后继续 `raise` 或转成更具体的异常。
8. 在 Python 代码中优先传 `argv list` 给 `subprocess.run(...)`。
9. 对 `requests` 调用显式设置 `timeout=`，不要把超时交给默认无限等待。
10. 在模块级创建 `logger = logging.getLogger(__name__)`，由命名 logger 负责输出。
11. 把 logging 配置集中到真正的 CLI 或应用启动层。

## 不要做（Don't）
1. 不要在公共函数签名中随手写 `Any` 作为兜底。
2. 不要让 payload、event、message、update 这类边界对象继续以匿名 `dict` / `Mapping` 形式跨模块漫游。
3. 不要把 `asyncio.create_task(...)` 直接丢成无主任务，也不要手动 new executor 却不收口生命周期。
4. 不要在 pure/core layer 里直接发 HTTP、开 socket、读写文件、拉 subprocess。
5. 不要在 core logic 里直接读当前时间、直接生成 UUID 或直接抽随机数。
6. 不要在 import 模块时直接创建 client、发请求、读文件、起后台任务或生成运行态随机值。
7. 不要写裸 `except:` 或 `except BaseException:`。
8. 不要吞掉广义 `Exception` 后假装成功。
9. 不要把 `Popen(...)` 当成普通命令执行的默认模板。
10. 不要用 `shell=True` 作为快捷方式。
11. 不要让 `requests` 在没有超时的情况下无限挂起，也不要用 `timeout=None` 关闭 `httpx` 超时。
12. 不要在 library-style 模块里直接 `logging.info(...)` 或 `logging.basicConfig(...)`。

## 最小验收
1. 新增与修改的公共函数具备完整类型注解。
2. payload-like 公共接口没有继续把原始 `dict` / `Mapping` 暴露成边界合同。
3. `asyncio.create_task(...)` 不存在被直接丢弃的无主任务，executor 生命周期由 `with` 显式托管。
4. pure/core layer 没有直接承载网络、文件、socket、subprocess 等真实 I/O。
5. core logic 不会直接读取当前时间、UUID 或随机性。
6. import 模块时不会直接做 runtime I/O、client/executor 初始化或 background task 启动。
7. 默认 Python 命令执行使用 `subprocess.run(...)`，且没有 `shell=True`。
8. 外部 HTTP 调用不会以“无超时”或“显式关闭超时”的形式长期悬挂。
9. 非 CLI 模块全部使用命名 logger，且不修改 root logging 配置。
10. 违反以上规则时，`python3 scripts/run_python_code_lints.py --target <target_root>` 返回非零退出码。
