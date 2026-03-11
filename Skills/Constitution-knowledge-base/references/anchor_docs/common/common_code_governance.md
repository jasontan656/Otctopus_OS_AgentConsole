# 通用锚点：code_governance（代码治理合同，阈值联动版）

anchor_id: `common_code_governance`
category: `common`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 将代码质量、拆分质量、目录质量统一为可执行治理合同。
- 将结构、契约与边界治理统一为可执行合同。
- 防止“逻辑可跑但结构失控”的隐性债务持续累积。

## 适用范围（必须全覆盖）

| 资产类型 | 治理焦点 |
|---|---|
| `backend` | 类型契约、错误码、分层职责、阈值拆分 |
| `database` | 迁移单职责、schema 稳定、repo 边界 |
| `tooling` | 脚本单职责、参数边界、校验可阻断 |
| `rule_files` | 规则定义纯度、1000 行上限、子域拆分 |

## 写法风格（命令式）
- 先写治理输入，再写判定规则，再写阻断条件。
- 每条规则必须对应至少一个可执行检查动作。
- 禁止描述性口号，必须使用可验证语句。

## 与 `common_file_structure` 的联动规则

1. 结构治理必须遵循 `common_file_structure` 的固定职责落点模板。
2. 规则类文件仅在“规则定义纯文件”前提下可使用 1000 行上限。
3. Python 胖文件阈值与拆分规则已迁移到 `Dev-PythonCode-Constitution-Backend`。

## 代码执行合同（Project Required）

| 项 | 规则 |
|---|---|
| 命名一致性 | 同语义仅一个主命名，禁止同义混名 |
| 错误边界 | 业务错误与系统错误分层，统一错误码 |
| 类型边界 | 输入输出模型显式定义并版本化 |
| 分层边界 | controller/page 不承载域规则与外部 I/O 细节 |
| 结构联动 | 拆分后文件必须落在固定职责模板路径 |
| 校验阻断 | CI 校验失败必须非零退出并阻断 |

## 扩展合同（按需）
- `risk_level`: 改动风险等级，驱动额外检查项。
- `change_scope`: 影响面范围定义，用于评审抽样。
- `quality_budget`: 技术债预算配额，超额禁止合并。
- `owner`: 当前改动治理责任人。

## 零豁免条款（No Waiver）

1. 不允许临时例外、口头例外、紧急例外。
2. 不允许“先超限后重构”。
3. 不允许通过改名、压缩空行、拆注释等伪方式规避阈值。
4. 不允许把业务实现塞入规则文件规避普通文件上限。

## 必须做（Do）
1. 新增功能先选择文件职责边界并确认固定落点。
2. 需要 Python 胖文件阈值时，转入 `Dev-PythonCode-Constitution-Backend`。
3. 关键改动必须同时更新类型、错误码和验证用例。
4. 每次跨层改动都要检视依赖方向是否破坏分层。
5. PR 必须附带“阈值 + 结构 + 兼容性”三类检查结果。

## 不要做（Don't）
1. 不要在 controller/page 中堆叠业务规则与外部调用。
2. 不要把 helper 写成隐式状态或 I/O 容器。
3. 不要把超限解释为“此处特殊”而跳过治理。
4. 不要在一个提交中混入无关重构与功能变更。
5. 不要保留不可解释魔法值和硬编码常量。

## 为什么（Why）
1. 结构治理若没有固定落点模板，最终仍会回到巨无霸文件。
2. 固定职责模板可显著降低定位成本与回归范围。
3. 零豁免能阻止“个案例外”持续侵蚀工程纪律。
4. 规则文件放宽上限但保持纯度，可兼顾可读性与工程现实。

## 实操命令（项目级）
```bash
# 1) 代码治理锚点反查
rg -n "common_code_governance|common_file_structure" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/common

# 2) 高风险标记巡检
rg -n "TODO|FIXME|HACK|WAIVER|waiver|临时豁免" . | head

# 3) helper 纯度检查（出现 I/O 关键词即告警）
find . -type f \( -name "*helper*.py" -o -name "*helper*.ts" \) -print0 | \
  xargs -0 rg -n "requests\\.|httpx\\.|fetch\\(|redis\\.|sqlalchemy|psycopg|subprocess|socket"

# 4) 规则类文件上限检查
find . -type f \( -name "*rule*.yaml" -o -name "*constitution*.md" -o -name "*lint*.yaml" \) -print0 | \
  xargs -0 wc -l | awk '$1>1000{print;bad=1} END{exit bad}'
```

## 最小验收
1. 结构化职责边界清晰且无越层实现。
2. 需要拆分的文件都能按 `common_file_structure` 固定落点完成拆分。
3. CI 对“结构 + 契约”校验失败时可阻断合并/发布。
4. PR 中不存在任何 waiver 或绕过记录。
