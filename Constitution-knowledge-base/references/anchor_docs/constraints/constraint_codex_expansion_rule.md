# 限制项：codex_expansion_rule（Codex 运行时扩展执行规则）

anchor_id: `constraint_codex_expansion_rule`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 约束 Codex 运行时相关输出必须联动后端、数据库和通用治理域。
- 防止把 `codex exec/session/resume/reply` 当无状态命令处理。
- 确保会话保持、幂等、重试、审计要求在输出中始终存在。

## 适用范围（必须全覆盖）

| 触发关键词域 | 必扩展域 |
|---|---|
| `codex/exec` | `codex_runtime_domain + backend_domain + database_domain + common_always_on` |
| `session_id/resume/reply` | 同上四域并集 |
| `wsl/cli_session` | 同上四域并集 |

## 写法风格（命令式）
- 先判定运行时触发，再挂域并集，再校验会话主题。
- 必须描述状态机，不允许只描述单条命令。
- 缺 `session` 关联策略时必须阻断。

## 触发扩展合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `codex/exec/session_id/resume/reply/wsl` 任一命中 |
| `required_domains` | 必须附 `codex_runtime_domain/backend_domain/database_domain/common_always_on` |
| `required_topics` | 必含会话保持、幂等键、失败重试、执行审计 |
| `session_binding` | 必须定义 `session_id` 与状态存储映射 |
| `missing_policy` | 缺域或缺主题返回 `missing_codex_expansion_domain` 并阻断 |

## 扩展合同（按需）
- `resume_window`: 会话恢复时间窗口。
- `idempotency_ttl`: 幂等键过期策略。
- `command_safety_profile`: 高风险命令限制模板。
- `execution_owner`: 运行时链路责任人。

## 必须做（Do）
1. 命中 Codex 运行时关键词时自动挂载四域并集。
2. 输出必须包含会话保持、幂等、重试、审计四项。
3. 必须定义 `session_id` 的存储与恢复策略。
4. 缺域或缺主题时立即阻断并返回缺失项。
5. 发布前执行 Codex 扩展完整性检查，失败阻断。

## 不要做（Don't）
1. 不要把 Codex 命令当无状态调用建议。
2. 不要忽略执行结果落库和回放要求。
3. 不要省略失败重试和超时边界。
4. 不要缺少审计字段约束。

## 为什么（Why）
1. Codex 交互本质是会话状态机而不是一次性命令。
2. 无数据库与审计约束会导致会话不可恢复、行为不可追溯。
3. 幂等和重试缺失会放大并发执行风险。
4. 强制并集可减少运行时不一致问题。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_codex_expansion_rule" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 图触发词检查
rg -n "trigger_any_of:.*codex|exec|session_id|resume|reply|wsl" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 域并集检查
rg -n "codex_runtime_domain|backend_domain|database_domain|common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 4) 缺失阻断事件检查
jq -c 'select(.status=="blocked" and .error_code=="missing_codex_expansion_domain")' logs/*.jsonl | head

# 5) 会话主题完整性检查
rg -n "session_id|幂等|重试|审计|resume" references/anchor_docs -S | head -n 300
```

## 最小验收
1. Codex 关键词命中输出四域并集附带率达到 100%。
2. 缺 `session` 绑定策略场景全部阻断，无放行。
3. 会话/幂等/重试/审计主题完整度覆盖率达到 100%。
4. 扩展判定可审计可回放。
