# 限制项：task_package_constitution_binding（任务包宪法锚点绑定执行合同）

anchor_id: `constraint_task_package_constitution_binding`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 强制任务包生成/更新时把宪法锚点证据显式绑定到任务包内容。
- 防止模型在长上下文下遗漏本次实际命中的宪法约束。
- 保证人类叙事层和机械任务层同时携带可机审的宪法约束。

## 适用范围（必须全覆盖）

| 场景 | 必须动作 |
|---|---|
| `task_package_generate` | 读取关键词并定位宪法锚点 |
| `task_package_update` | 重新评估关键词并补齐缺失锚点 |
| `task_package_review` | 检查锚点引用完整性并输出缺失清单 |
| `task_package_execute_handoff` | 输出可执行约束索引与证据引用 |

## 写法风格（命令式）
- 先写关键词定位规则，再写锚点绑定规则，再写阻断规则。
- 必须可机器验证，不允许建议式描述。
- 缺失项必须结构化返回，不允许口头确认放行。

## 绑定执行合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `任务包/task package/work package/L1/L2/L3` 任一命中即触发 |
| `keyword_source` | 必须由任务目标、阶段描述、约束条款提取双语关键词 |
| `anchor_lookup` | 必须通过宪法关键词查询工具定位锚点，不允许手工猜测 |
| `required_matched_anchors` | 必须绑定本次查询真实命中的锚点；禁止凭记忆补写未命中锚点 |
| `required_constraints` | 如查询命中 `constraint_task_package_constitution_binding`，则该约束自身必须进入绑定清单 |
| `narrative_binding_target` | 人类叙事板块必须包含 `governance_obligations/acceptance_gate/static_lint_contract` |
| `machine_binding_target` | 机械任务文件必须包含 `anchor_bindings[]`，每项必填 `anchor_id/clause_ref/binding_reason/target_block/evidence_ref` |
| `missing_policy` | 缺失锚点或绑定目标时返回 `insufficient_constitution_binding` 并阻断 |

## 必须做（Do）
1. 任务包生成前先做双语关键词提取并调用宪法查询工具。
2. 查询命中结果必须映射为任务包锚点清单并落到人类叙事板块。
3. 同一批锚点必须同步落到机械任务文件的 `anchor_bindings[]`。
4. 每个锚点至少绑定一个可验证目标块，不允许悬空引用。
5. 任务包更新时必须执行差异检查并补齐新增/变更锚点。
6. 发布或执行前必须跑绑定完整性检查，失败即阻断。

## 不要做（Don't）
1. 不要只在说明文字提到“遵守宪法”而不写具体锚点。
2. 不要只更新人类叙事而漏掉机械任务文件。
3. 不要在无证据引用时放行任务包。
4. 不要用人工记忆替代查询工具自动挂钩。

## 为什么（Why）
1. 任务包是执行入口，若无锚点绑定会出现设计合规、执行跑偏。
2. 双层绑定（叙事+机械）可同时服务人审与机审。
3. 结构化阻断能避免上下文丢失带来的规则遗漏。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_task_package_constitution_binding" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 查询结果与任务包锚点字段检查
rg -n "anchor_bindings|anchor_id|clause_ref|binding_reason|target_block|evidence_ref" OctuposOS_Runtime_Backend -S

# 3) 查询入口检查
rg -n "constitution_keyword_query|minimum_keyword_contract|constitution_enforcement_contract" Skills/Constitution-knowledge-base -S
```

## 最小验收
1. 任务包类请求命中后，本次查询命中的锚点全部进入绑定清单。
2. 每个任务包同时存在人类叙事绑定和机械绑定清单。
3. `anchor_bindings[]` 每项都具备 `anchor_id/clause_ref/binding_reason/target_block/evidence_ref`。
4. 缺失绑定场景全部被阻断，无放行记录。
