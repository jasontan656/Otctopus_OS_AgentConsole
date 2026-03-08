# 通用锚点：fat_file（胖文件治理合同，零豁免强制版）

anchor_id: `common_fat_file`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制把实现拆成小职责文件，避免“巨无霸文件”吞掉可维护性。
- 固定工程拆分形态：orchestrator + domain + adapter + helper，不允许随意混写。
- 将“行数限制”从建议升级为发布阻断条件。

## 适用范围（必须全覆盖）

| 资产域 | 受约束文件 |
|---|---|
| `backend` | `.py` 业务实现、API、worker、repository、adapter |
| `frontend` | `.ts/.vue` 页面、组件、状态管理、API 客户端、helper |
| `database` | repository、model、migration、schema |
| `tooling` | CLI 脚本、构建脚本、校验脚本 |
| `rule_files` | lint/rule/policy/constitution 规则类定义文件 |

## 写法风格（命令式）
- 先写文件类别，再写上限，再写超限动作。
- 拆分规则必须对应固定落点，不写抽象建议。
- 违规条件必须可在 CI 中自动判定。

## 文件行数矩阵（强制硬上限）

| 文件类别 | 上限（行） | 说明 |
|---|---:|---|
| `backend_api_controller` | 220 | 只做入口校验、路由分发、响应拼装。 |
| `backend_orchestrator` | 180 | 只做流程编排，不写具体业务规则。 |
| `backend_domain_service` | 260 | 只放业务规则和领域决策。 |
| `backend_repository_or_model` | 220 | 只放持久化读写与模型映射。 |
| `backend_adapter_client` | 220 | 只放外部系统交互适配。 |
| `backend_helper` | 140 | 纯函数与通用小工具。 |
| `frontend_page_container` | 220 | 页面组装与路由态，不写复杂逻辑。 |
| `frontend_component_view` | 160 | 展示组件，只处理视图逻辑。 |
| `frontend_store_or_composable` | 180 | 状态流与副作用协调。 |
| `frontend_api_client` | 160 | 请求映射、错误映射、重试策略。 |
| `frontend_helper` | 120 | 纯函数 helper。 |
| `db_migration_file` | 180 | 单次迁移单职责。 |
| `schema_or_contract_file` | 300 | 类型/契约定义，不混业务流程。 |
| `workflow_or_contract_support` | 240 | `scripts/` 下的流程合同、策略支持、阶段支持类文件。 |
| `registry_or_contract_data` | 280 | `scripts/` 下的 registry/data/映射类文件。 |
| `cli_or_task_script` | 220 | 参数解析 + 单一任务执行；必须具备明确 CLI 入口特征。 |
| `unit_test_file` | 260 | 单模块测试。 |
| `integration_e2e_test_file` | 420 | 允许更长，但必须按场景分段。 |
| `runtime_config_file` | 180 | 仅配置映射，不写业务流程。 |
| `rule_definition_file` | 1000 | 仅限规则类文件（lint/policy/rule/constitution）。 |

## 固定职责拆分模板（必须遵守）

### Backend 固定模板
1. `<feature>_controller.py`：参数校验、鉴权、调用 orchestrator、返回标准响应。
2. `<feature>_orchestrator.py`：串联 domain/repo/adapter，处理流程顺序和补偿。
3. `<feature>_domain.py`：纯业务规则与决策，不访问外部 I/O。
4. `<feature>_repo.py`：数据库读写、查询拼装、事务边界。
5. `<feature>_adapter_<target>.py`：外部系统调用、协议映射、重试策略。
6. `<feature>_helper.py`：纯函数工具，禁止持久化和网络 I/O。

### Frontend 固定模板
1. `<Feature>Page.vue`：页面编排、路由参数、状态挂载。
2. `<Feature>Panel*.vue`：展示组件，禁止网络请求。
3. `use<Feature>Flow.ts`：状态机/流程控制。
4. `<feature>.api.ts`：接口调用与错误映射。
5. `<feature>.helper.ts`：纯函数 helper。

### Rule 文件固定模板
1. 规则类文件允许到 1000 行，但必须仅包含规则定义。
2. 规则类文件禁止内嵌业务实现代码。
3. 超过 1000 行必须按子域拆分为多个规则文件。

### Tooling/Contracts 固定模板
1. `*_cli.py` / `*_task.py` / `*_runner.py`：显式命令入口、参数解析、单一任务执行。
2. `*workflow*_support.py` / `*policy*_support.py`：流程规则辅助与阶段支持，不等同 CLI。
3. `*registry*.py` / `*data*.py`：映射、注册表、常量数据面，不等同 CLI。
4. `*contract*.py`：契约/结构/阶段定义，优先按 contract/support 分类治理。

## 扩展合同（按需）
- `enforcement_profile`: 不同仓库可选择的治理检查组合。
- `exempt_scope`: 仅记录不可避免特殊资产范围，不等于豁免。
- `split_ref`: 超限拆分任务与 PR 关联标识。
- `owner`: 超限整改责任人。

## 胖文件治理合同（Project Required）

| 项 | 规则 |
|---|---|
| `category_mapping` | 每个文件必须映射到唯一文件类别 |
| `line_threshold` | 行数不得超过对应类别硬上限 |
| `split_deadline` | 达阈值 85% 必须预拆分，100% 前完成 |
| `target_layout` | 拆分后必须落到固定职责模板 |
| `check_blocking` | 违规检查必须阻断合并和发布 |

## 零豁免条款（No Waiver）

1. 禁止任何 waiver、临时豁免、口头豁免、灰度豁免。
2. 禁止“先合并后拆分”。
3. 超上限文件一律阻断合并与发布。
4. 任何人、任何分支、任何紧急场景均不得绕过本条款。

## 必须做（Do）
1. 新增功能先选定文件类别，再按矩阵控制行数。
2. 触碰上限前先拆分，不得超限后补救。
3. 拆分必须按固定职责模板落地。
4. PR 检查必须包含文件行数矩阵校验并以非零退出码阻断。
5. 规则类文件必须显式标记为 `rule_definition_file` 才能享受 1000 行上限。

## 不要做（Don't）
1. 不要在 controller/page 中堆叠业务规则与外部调用。
2. 不要把 helper 写成隐式状态容器。
3. 不要把超限合理化为“这个文件特殊”。
4. 不要把规则文件当业务实现收容器。
5. 不要通过拆注释、压缩行宽等伪手段规避治理。

## 为什么（Why）
1. 小职责文件是高并发协作和快速排障的基础。
2. 固定模板让模型和人都能稳定定位逻辑位置。
3. 零豁免可以杜绝“例外累积”导致治理失效。
4. 规则文件放宽到 1000 行，解决你指出的 lint/policy 类误伤问题。

## 实操命令（项目级）
```bash
# 1) 全量查看超长文件（快速巡检）
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.vue" -o -name "*.sql" -o -name "*.yaml" -o -name "*.yml" \) \
  -not -path "*/.git/*" -print0 | xargs -0 wc -l | sort -nr | head -n 200

# 2) helper 文件强约束（>120 直接失败）
find . -type f \( -name "*helper*.py" -o -name "*helper*.ts" \) -print0 | \
  xargs -0 wc -l | awk '$1>120{print;bad=1} END{exit bad}'

# 3) 规则类文件上限检查（>1000 失败）
find . -type f \( -name "*rule*.md" -o -name "*rule*.yaml" -o -name "*lint*.yaml" -o -name "*constitution*.md" \) -print0 | \
  xargs -0 wc -l | awk '$1>1000{print;bad=1} END{exit bad}'

# 4) 本条款反查
rg -n "common_fat_file" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml
```

## 最小验收
1. 非规则类文件无任何超矩阵上限项。
2. 规则类文件全部 <= 1000 行，且仅包含规则定义。
3. 任意超限文件会在 CI 中被阻断（非零退出码）。
4. PR 中不存在 waiver 语句、临时豁免说明或绕过记录。
