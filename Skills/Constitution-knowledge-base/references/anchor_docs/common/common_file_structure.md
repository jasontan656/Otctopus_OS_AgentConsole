# 通用锚点：file_structure（文件结构合同）

anchor_id: `common_file_structure`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 规定超限或复杂实现时必须按固定职责拆分并落到固定位置，不允许随意新建杂项文件。
- 规定超阈值后必须按固定职责拆分并落到固定位置，不允许随意新建杂项文件。
- 保证 helper 抽象、职责分离、目录清洁可以机械执行。

## 适用范围（必须全覆盖）

| 域 | 受约束对象 |
|---|---|
| `backend` | controller/orchestrator/domain/repo/adapter/helper |
| `database` | migration/schema/repository |
| `tooling` | cli/task/check scripts |
| `rule_files` | lint/policy/rule/constitution 定义文件 |

## 写法风格（命令式）
- 先写目录落点，再写职责边界，再写越层禁令。
- 每个约束都要明确违规判定标准。
- 拆分动作必须能映射到固定模板路径。

## 固定拆分落点规则

1. `common_file_structure` 只定义“复杂实现或需拆分时的固定落点”。
2. 规则类文件仍必须遵循单一规则域。
3. Python 胖文件阈值已迁移到 `Dev-PythonCode-Constitution-Backend`。

## 固定目录与文件职责模板（必须遵守）

### Backend
```text
<feature>/
├── <feature>_controller.py      # 参数校验/鉴权/响应拼装
├── <feature>_orchestrator.py    # 流程编排/补偿顺序
├── <feature>_domain.py          # 业务规则与决策
├── <feature>_repo.py            # 数据读写与事务边界
├── <feature>_adapter_<x>.py     # 外部协议适配
└── <feature>_helper.py          # 纯函数工具
```

### Database / Rule
```text
<feature>/
├── migration_*.sql              # 单次迁移单职责
├── <feature>.schema.ts          # 契约/模型定义
└── rules/
    ├── <domain>_rule_*.yaml     # 规则定义（仅规则）
    └── <domain>_constitution.md # 规则说明（仅规则）
```

## 阈值触发后的拆分矩阵（结构联动）

| 文件类别 | 需要拆分时必须拆到 |
|---|---|
| `backend_api_controller` | `*_controller.py` + `*_orchestrator.py` |
| `backend_orchestrator` | `*_orchestrator.py` + `*_domain.py` |
| `backend_domain_service` | `*_domain.py` + `*_helper.py` |
| `backend_repository_or_model` | `*_repo.py` + `*.schema.*` |
| `backend_adapter_client` | `*_adapter_<x>.py` + `*_helper.py` |
| `cli_or_task_script` | `cli_entry.*` + `task_runner.*` + `helper.*` |
| `rule_definition_file` | `rules/<subdomain>_rule_*.yaml` 多文件分域 |

## 文件结构合同（Project Required）

| 项 | 规则 |
|---|---|
| 单文件职责 | 一个文件只能有一个主职责 |
| 目录落点 | 文件必须落在固定模板路径 |
| 入口约束 | controller/page 为入口，其它层不可反向越层调用 |
| helper 约束 | helper 只允许纯函数，不允许 I/O 与状态持有 |
| 规则文件约束 | 规则文件只写规则定义，不写业务执行代码 |

## 扩展合同（按需）
- `module_index`: 模块目录索引文件，约束公开接口。
- `dep_graph_ref`: 目录依赖图引用，用于越层检查。
- `ownership_map`: 目录到责任人的映射。
- `migration_plan_ref`: 目录重构迁移计划引用。

## 零豁免条款（No Waiver）

1. 不允许任何临时例外、口头例外、紧急例外。
2. 不允许“先超限后重构”。
3. 不允许通过改名、拆注释等伪方式规避阈值治理。
4. 不允许将超限逻辑塞进规则文件规避普通文件上限。

## 必须做（Do）
1. 新功能创建时按固定模板一次性建好分层文件。
2. 达到阈值预警即拆分，不等到超限。
3. 拆分后保持外部接口兼容并补验证。
4. 目录重构必须同步更新导入路径和文档引用。
5. CI 中执行阈值与路径双校验，失败即阻断。

## 不要做（Don't）
1. 不要把 controller/page 写成巨型业务实现文件。
2. 不要让 domain/repo/adapter/helper 职责交叉。
3. 不要在 helper 中访问数据库、网络、全局可变状态。
4. 不要把规则文件当“超长业务逻辑收纳箱”。

## 为什么（Why）
1. 阈值没有结构落点就无法执行，最终会回到巨无霸。
2. 固定模板让团队与模型都能快速定位改动位置。
3. 零豁免能防止治理被“个案例外”逐步掏空。

## 实操命令（项目级）
```bash
# 1) 结构模板命中检查（按命名扫描）
find . -type f | rg -n "_controller\\.py|_orchestrator\\.py|_domain\\.py|_repo\\.py|_adapter_|helper\\.(py|ts)$|Page\\.vue|Panel"

# 2) helper 纯度检查（禁止出现典型 I/O 关键词）
find . -type f \( -name "*helper*.py" -o -name "*helper*.ts" \) -print0 | \
  xargs -0 rg -n "requests\\.|httpx\\.|fetch\\(|redis\\.|sqlalchemy|psycopg|subprocess|socket"

# 3) 规则文件目录与上限检查
find . -type f \( -name "*rule*.yaml" -o -name "*constitution*.md" -o -name "*lint*.yaml" \) -print0 | \
  xargs -0 wc -l | awk '$1>1000{print;bad=1} END{exit bad}'

# 4) 本条款反查
rg -n "common_file_structure" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common
```

## 最小验收
1. 超阈值文件都能映射到固定拆分落点并已拆分。
2. helper 文件不包含 I/O 与状态持有逻辑。
3. 规则类文件全部 <= 1000 行且仅包含规则定义。
4. CI 对“行数 + 结构”双校验失败时可阻断合并/发布。
