# 限制项：always_attach_common（common_core 强制挂载执行合同）

anchor_id: `constraint_always_attach_common`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制任何关键词命中结果都附带 `common_core` 静态治理底座。
- 防止只返回域内条款而缺失结构、契约与边界约束。
- 统一不同域输出的最低可 gate 完整度。

## 适用范围（必须全覆盖）

| 场景 | 约束目标 |
|---|---|
| `keyword_retrieval` | 关键词检索结果必须挂通用锚点 |
| `design_response` | 架构建议必须附通用静态治理 |
| `implementation_response` | 实施建议必须附结构与契约约束 |
| `task_package_response` | 任务包建议必须附任务包宪法绑定约束 |

## 写法风格（命令式）
- 先写挂载条件，再写必挂集合，再写阻断动作。
- 仅使用可判定规则，不写建议语句。
- 缺失项必须返回结构化缺失清单。

## 触发挂载合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_scope` | 命中任意业务域关键词即触发 |
| `required_node` | 必挂 `common_core` |
| `required_anchors` | 必含 `common_code_governance/common_file_structure/common_folder_structure/common_modularity/common_typed_contract/common_permission_boundary` |
| `required_constraints` | 任务包生成与更新场景必须附 `constraint_task_package_constitution_binding` |
| `missing_policy` | 缺任一项返回 `insufficient_evidence` 并阻断 |
| `trace_flag` | 查询结果必须显式给出 `required_common_anchors` |

## 必须做（Do）
1. 先挂 `common_core`，再挂域内锚点。
2. 输出中必须显式出现通用锚点集合。
3. 缺失通用锚点时立即阻断并返回缺失项。
4. 命中任务包语义时必须追加任务包宪法绑定约束。
5. 查询 contract 校验必须覆盖 `required_common_anchors` 与 `required_constraint_anchors`。

## 不要做（Don't）
1. 不要输出不带通用约束的单域建议。
2. 不要把 `common_core` 当可选项。
3. 不要用人工口头确认替代机器检查。
4. 不要保留已删除锚点的死引用。

## 为什么（Why）
1. 通用约束是跨域一致性最小底座。
2. 先挂治理再挂领域能减少后期补洞成本。
3. 强阻断可防止“领域命中但治理缺席”的输出进入实施。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_always_attach_common" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) common_always_on 图节点检查
rg -n "common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 必挂锚点集合检查
rg -n "common_code_governance|common_file_structure|common_folder_structure|common_modularity|common_typed_contract|common_permission_boundary" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml

# 4) 任务包绑定约束检查
rg -n "constraint_task_package_constitution_binding" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml
```

## 最小验收
1. 关键词命中结果始终带完整 `required_common_anchors`。
2. 已删除锚点不再出现在必挂集合。
3. 任务包类请求命中时，任务包绑定约束覆盖率为 100%。
4. 查询 contract 校验可在 CI 自动执行并阻断失败构建。
