# 限制项：database_expansion_rule（数据库扩展执行规则）

anchor_id: `constraint_database_expansion_rule`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 约束数据库相关输出必须联动后端域和通用治理域。
- 防止孤立 SQL 建议脱离调用语义和审计约束。
- 保证读写边界、生命周期、回放键和回滚策略完整。

## 适用范围（必须全覆盖）

| 触发关键词域 | 必扩展域 |
|---|---|
| `database/persistence/storage` | `database_domain + backend_domain + common_always_on` |
| `cache/session_store/replay_store` | 同上三域并集 |
| `audit_log/index/migration` | 同上三域并集 |

## 写法风格（命令式）
- 先判定数据库命中，再挂后端与通用域。
- 必须写谁读写、何时写、如何回滚。
- 缺访问路径定义时必须阻断。

## 触发扩展合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `database/persistence/cache/audit_log/session_store` 任一命中 |
| `required_domains` | 必须附 `database_domain/backend_domain/common_always_on` |
| `required_topics` | 必含读写边界、索引策略、保留周期、回放键设计 |
| `access_path_required` | 必须给出调用方与访问路径 |
| `missing_policy` | 缺域或缺访问路径返回 `missing_database_expansion_domain` 并阻断 |

## 扩展合同（按需）
- `retention_policy`: 数据保留与清理策略。
- `partition_policy`: 分区与冷热分层策略。
- `backup_policy`: 备份与恢复策略。
- `consistency_level`: 一致性级别说明。

## 必须做（Do）
1. 命中数据库关键词时自动挂载三域并集。
2. 输出必须写访问路径、索引、生命周期、回放键。
3. 缺调用方定义时立即阻断并返回补证项。
4. 缓存建议必须声明主存储与失效策略。
5. 发布前执行数据库扩展完整性检查，失败阻断。

## 不要做（Don't）
1. 不要只给 SQL 片段不解释调用边界。
2. 不要把缓存当唯一真值来源。
3. 不要忽略审计留存和回滚可行性。
4. 不要省略事务与一致性语义。

## 为什么（Why）
1. 数据层正确性取决于调用语义而非表结构本身。
2. 生命周期和回放键缺失会让审计与恢复失效。
3. 强制并集能避免“数据建议孤岛化”。
4. 可执行阻断可前移发现缺失设计。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_database_expansion_rule" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 图触发词检查
rg -n "trigger_any_of:.*database|persistence|cache|audit_log|session_store" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 域并集检查
rg -n "database_domain|backend_domain|common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 4) 缺失阻断事件检查
jq -c 'select(.status=="blocked" and .error_code=="missing_database_expansion_domain")' logs/*.jsonl | head

# 5) 数据主题完整性检查
rg -n "索引|生命周期|回放键|保留周期|访问路径" references/anchor_docs -S | head -n 300
```

## 最小验收
1. 数据库关键词命中输出三域并集附带率达到 100%。
2. 缺访问路径场景全部阻断，无放行记录。
3. 读写边界/索引/生命周期/回放主题完整度覆盖率达到 100%。
4. 缓存建议均包含失效与一致性说明。
