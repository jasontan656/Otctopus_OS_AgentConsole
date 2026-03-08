# 限制项：telegram_expansion_rule（Telegram 扩展执行规则）

anchor_id: `constraint_telegram_expansion_rule`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 约束 Telegram 相关输出必须覆盖渠道、后端、数据库与通用治理四域并集。
- 防止只给 Bot 代码片段而缺失回执链路、会话隔离等关键要素。
- 让 Telegram 场景建议直接具备可落地和可运维性。

## 适用范围（必须全覆盖）

| 触发关键词域 | 必扩展域 |
|---|---|
| `telegram/bot` | `telegram_channel_domain + backend_domain + database_domain + common_always_on` |
| `webhook/callbackquery/inline_button` | 同上四域并集 |
| `deep_link/sendDocument/webapp` | 同上四域并集 |

## 写法风格（命令式）
- 先判定 Telegram 触发，再挂四域并集，再校验主题完整性。
- 输出必须写链路，不允许单点实现建议。
- 缺域立即阻断并返回缺失项。

## 触发扩展合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `telegram/webhook/callbackquery/inline_button/deep_link/sendDocument/webapp` 任一命中 |
| `required_domains` | 必须命中四域并集 |
| `required_topics` | 必含回执策略、重试策略、消息映射、会话绑定、权限边界 |
| `webapp_rule` | WebApp 场景如存在，必须包含 session 绑定策略 |
| `missing_policy` | 缺域或缺主题返回 `missing_telegram_expansion_domain` 并阻断 |

## 扩展合同（按需）
- `rate_limit_policy`: 渠道限流与退避策略。
- `media_policy`: 文档/媒体消息大小与存储策略。
- `callback_ttl`: 回调按钮有效期与失效动作。
- `anti_abuse_policy`: 防刷与风控策略。

## 必须做（Do）
1. 命中 Telegram 关键词时强制挂载四域并集。
2. 输出必须写消息回执、失败重试、映射规则。
3. WebApp 场景如存在，必须写会话隔离策略。
4. 缺域或缺主题时立即阻断并返回结构化缺失项。
5. 发布前执行 Telegram 扩展完整性检查，失败阻断。

## 不要做（Don't）
1. 不要只给 Bot API 调用代码。
2. 不要忽略 WebApp 场景下的协议一致性。
3. 不要忽略权限边界和审计要求。
4. 不要省略失败回执与重试策略。

## 为什么（Why）
1. Telegram 场景天然是多域耦合链路。
2. 缺任一域会导致交互断链或不可审计。
3. 四域并集是把“能回复消息”升级为“可运营系统”的最低条件。
4. 强阻断机制可把漏项前移到设计阶段。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_telegram_expansion_rule" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 图触发词检查
rg -n "trigger_any_of:.*telegram|webhook|callbackquery|inline_button|deep_link|sendDocument|webapp" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 五域并集检查
rg -n "telegram_channel_domain|backend_domain|database_domain|common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 4) 缺失阻断事件检查
jq -c 'select(.status=="blocked" and .error_code=="missing_telegram_expansion_domain")' logs/*.jsonl | head

# 5) Telegram 输出主题完整性检查
rg -n "回执|重试|映射|会话|权限边界" references/anchor_docs -S | head -n 300
```

## 最小验收
1. Telegram 命中输出五域并集附带率达到 100%。
2. WebApp 场景如存在，session 绑定策略覆盖率达到 100%。
3. 缺域阻断命中率为 100%，无漏放行。
4. 回执/重试/映射/会话/权限主题完整度覆盖率达到 100%。
