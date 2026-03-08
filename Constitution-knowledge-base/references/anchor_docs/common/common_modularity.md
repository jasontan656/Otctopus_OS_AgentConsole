# 通用锚点：modularity（模块化与依赖边界合同）

anchor_id: `common_modularity`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 固定模块职责与依赖方向，防止业务逻辑在代码库中无序扩散。
- 让后端、前端、数据库、集成适配都可独立替换、独立测试、独立发布。
- 为 `common_fat_file` 与 `common_file_structure` 提供“拆分后该放哪里、能依赖谁”的硬约束。

## 适用范围（必须全覆盖）

| 模块域 | 最小模块集合 |
|---|---|
| `backend` | `controller`, `orchestrator`, `domain`, `repository`, `adapter`, `helper` |
| `frontend` | `page`, `panel/component`, `flow/composable`, `api_client`, `helper` |
| `database` | `migration`, `schema/contract`, `repository` |
| `runtime_tooling` | `cli_entry`, `task_runner`, `validator/checker` |
| `shared` | `shared_types`, `shared_errors`, `shared_utils` |

## 写法风格（命令式）
- 先写边界，再写依赖，再写禁止项。
- 只写可执行规则，不写口号式描述。
- 每条规则必须能被检查脚本或代码评审直接判定。

## 分层依赖合同（Project Required）

| 层 | 允许依赖 | 禁止依赖 |
|---|---|---|
| `controller/page` | `orchestrator/flow`, `shared_types`, `shared_errors` | `repository`, `adapter`, `db driver` |
| `orchestrator/flow` | `domain`, `repository`, `adapter`, `shared_*` | `controller/page` 反向依赖 |
| `domain` | `shared_types`, `shared_errors`, `helper` | `repository`, `adapter`, `http client`, `db client` |
| `repository` | `schema/contract`, `db driver`, `shared_errors` | `controller/page`, `domain` 反向调用 |
| `adapter` | 外部 SDK/HTTP client, `shared_errors` | `controller/page`, `domain` 内部状态访问 |
| `helper` | 标准库、纯函数依赖 | 网络 I/O、数据库 I/O、全局可变状态 |

## 模块接口合同（Project Required）

| 项 | 规则 |
|---|---|
| `module_entry` | 每个模块仅 1 个稳定入口文件，其他文件视为内部实现 |
| `public_api` | 模块只暴露最小必要函数/类型，禁止导出内部工具 |
| `contract_version` | 跨模块契约变更必须标注版本或迁移说明 |
| `error_boundary` | 跨模块仅传递标准错误码，不透传底层异常对象 |
| `state_ownership` | 状态只能由一个模块拥有，其他模块只通过契约读写 |
| `change_scope` | 单次提交只允许一个主模块改动，跨模块改动必须列影响面 |

## 扩展合同（按需）
- `plugin_module`: 必须通过显式注册表接入，禁止动态扫描目录隐式注入。
- `feature_flag_module`: 只负责开关判定，禁止混入业务副作用。
- `integration_module`: 必须提供超时、重试、熔断策略，并独立测试。

## 必须做（Do）
1. 新功能先落模块边界图，再写实现代码。
2. 模块目录中必须有 `entry`、`internal`、`tests` 三类落点。
3. 每次新增跨模块调用都补契约说明与失败语义。
4. 达到文件阈值前先拆分为固定职责子模块，禁止超限后补拆。
5. 每次重构都验证“外部可观察行为不变”，只允许内部结构变化。
6. CI 必须包含循环依赖检查与分层依赖检查，失败即阻断。

## 不要做（Don't）
1. 不要跨模块直接访问内部文件、内部状态、内部常量。
2. 不要让 `domain` 直接调用数据库、HTTP、消息队列客户端。
3. 不要创建“万能 shared 模块”收纳业务逻辑。
4. 不要以“临时”理由引入反向依赖或循环依赖。
5. 不要在模块间传递未经约束的原始 payload。
6. 不要在 helper 中偷偷做 I/O 或缓存写入。

## 为什么（Why）
1. 模块边界稳定后，局部修改不会扩散成全局回归。
2. 单向依赖可把故障半径控制在一个模块域内。
3. 契约化接口可让多技术栈并行演进而不互相阻塞。
4. 把 I/O 与领域逻辑拆开后，测试与排障成本显著下降。

## 实操命令（项目级）

```bash
# 1) 锚点反查（确保条款已被索引）
rg -n "common_modularity" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common

# 2) 快速发现潜在循环依赖线索（同特性目录互相 import）
rg -n "^(from|import) " src backend frontend | head -n 300

# 3) 检查 domain 层是否误用 I/O 依赖（命中即整改）
find . -type f \( -name "*domain*.py" -o -name "*domain*.ts" \) -print0 | \
  xargs -0 rg -n "requests\\.|httpx\\.|fetch\\(|axios\\(|sqlalchemy|psycopg|redis\\.|pymongo|subprocess|socket"

# 4) 检查 helper 纯度（命中即整改）
find . -type f \( -name "*helper*.py" -o -name "*helper*.ts" \) -print0 | \
  xargs -0 rg -n "requests\\.|httpx\\.|fetch\\(|axios\\(|sqlalchemy|redis\\.|pymongo|subprocess|socket"
```

## 最小验收
1. 任取 1 个主功能模块，能明确指出 `entry/internal/tests` 三层落点。
2. 核心依赖图无循环依赖，且无反向越层调用。
3. `domain` 与 `helper` 抽检样本中 I/O 违规命中率为 0。
4. 任意跨模块契约变更均附版本或迁移说明。
