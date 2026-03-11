# 限制项：backend_expansion_rule（后端扩展执行规则）

anchor_id: `constraint_backend_expansion_rule`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 限制“后端命中”输出不得只停留在 API 层。
- 强制联动数据库域和通用治理域，形成完整执行链路。
- 避免后端建议缺失持久化、重试、审计、门禁要素。

## 适用范围（必须全覆盖）

| 触发关键词域 | 必扩展域 |
|---|---|
| `backend/api` | `backend_domain + database_domain + common_always_on` |
| `worker/queue` | `backend_domain + database_domain + common_always_on` |
| `webhook/gateway` | `backend_domain + database_domain + common_always_on` |

## 写法风格（命令式）
- 先判定命中，再判定扩展域，再判定阻断。
- 输出必须声明缺失项和补齐动作。
- 每条规则都要可由检索结果自动验证。

## 触发扩展合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `backend/api/worker/queue/webhook/gateway` 任一命中即触发 |
| `required_domains` | 必须同时包含 `backend_domain` 与 `database_domain` |
| `required_common` | 必须附带 `common_always_on` |
| `required_topics` | 必须包含接口契约、异步语义、持久化边界、可观测字段 |
| `missing_policy` | 缺任一域或主题即阻断并返回缺失清单 |

## 扩展合同（按需）
- `cache_policy`: 后端场景缓存一致性策略要求。
- `idempotency_policy`: 幂等键和去重策略要求。
- `retry_policy`: 重试与退避策略要求。
- `ownership_scope`: 负责模块和责任人映射。

## 必须做（Do）
1. 命中后端关键词时自动挂载 `backend_domain + database_domain + common_always_on`。
2. 输出必须含接口契约、任务语义、数据边界、观测字段。
3. 缺任一扩展域时返回结构化缺失项并阻断。
4. 后端输出必须附错误码和重试策略建议。
5. 发布前执行后端扩展完整性检查，失败阻断。

## 不要做（Don't）
1. 不要只返回路由或 handler 级建议。
2. 不要忽略数据库读写一致性与事务边界。
3. 不要缺失审计和门禁字段约束。
4. 不要在高风险写路径省略回滚入口。

## 为什么（Why）
1. 后端可运行不等于后端可运营。
2. API 与数据层脱节会直接引发线上一致性问题。
3. 通用治理缺失会让故障不可追溯。
4. 强制并集可减少“补规则返工”。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_backend_expansion_rule" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 图规则触发词检查
rg -n "trigger_any_of:.*backend|api|worker|queue|webhook|gateway" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 扩展域命中检查
rg -n "backend_domain|database_domain|common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 4) 缺失阻断事件抽检
jq -c 'select(.status=="blocked" and .error_code=="missing_backend_expansion_domain")' logs/*.jsonl | head

# 5) 后端输出主题完整性检查
rg -n "接口契约|异步|持久化|可观测|重试|错误码" references/anchor_docs/backend references/anchor_docs/common -S
```

## 最小验收
1. 后端关键词命中结果，`database_domain` 附带率达到 100%。
2. 缺域场景全部阻断，无放行记录。
3. 输出主题完整度（契约/异步/持久化/观测）覆盖率达到 100%。
4. 审计可回查每次扩展判定与阻断原因。
