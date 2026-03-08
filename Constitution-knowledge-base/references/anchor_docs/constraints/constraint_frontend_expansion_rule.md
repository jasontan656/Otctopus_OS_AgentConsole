# 限制项：frontend_expansion_rule（前端扩展执行规则）

anchor_id: `constraint_frontend_expansion_rule`
category: `constraints`
mol_resident_source:
- `assets/goal/MOL_FULL_CANON.md`
graph_hook:
- graph_doc: `references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md`
- graph_node: `common_always_on`

## 在项目中起什么作用
- 限制“前端命中”输出不得脱离后端契约与治理约束。
- 强制联动后端域和通用域，保证前端建议可真实落地。
- 避免纯 UI 方案进入实施后无法观测、无法审计、无法回滚。

## 适用范围（必须全覆盖）

| 触发关键词域 | 必扩展域 |
|---|---|
| `frontend/ui/page` | `frontend_domain + backend_domain + common_always_on` |
| `webapp/canvas/admin_ui` | `frontend_domain + backend_domain + common_always_on` |
| `telegram_webapp` | 额外附带 `telegram_channel_domain` |

## 写法风格（命令式）
- 先判定前端命中，再挂后端与通用域。
- 输出必须写接口契约与错误回执，不只写组件实现。
- 移动端或弱网场景必须写降级路径。

## 触发扩展合同（Project Required）

| 项 | 规则 |
|---|---|
| `trigger_any_of` | `frontend/ui/page/webapp/canvas/admin_ui` 任一命中 |
| `required_domains` | 必须附 `frontend_domain` 与 `backend_domain` |
| `required_common` | 必须附 `common_always_on` |
| `telegram_extra` | Telegram WebApp 场景必附 `telegram_channel_domain` |
| `required_topics` | 必含状态管理、接口契约、错误回执、权限可见性、降级路径 |

## 扩展合同（按需）
- `render_budget`: 首屏与交互性能预算。
- `offline_policy`: 弱网或离线降级策略。
- `interaction_audit`: 关键交互审计字段要求。
- `compatibility_matrix`: 终端兼容矩阵要求。

## 必须做（Do）
1. 命中前端关键词时自动挂载 `backend_domain + common_always_on`。
2. WebApp 场景自动补挂 `telegram_channel_domain`。
3. 输出必须写前后端契约和错误处理闭环。
4. 缺任一域或主题时立即阻断并返回缺失项。
5. 前端输出必须包含权限可见性和降级策略。

## 不要做（Don't）
1. 不要只给组件样式和页面结构建议。
2. 不要忽略接口契约和状态一致性。
3. 不要忽略移动端性能与弱网恢复路径。
4. 不要在前端输出中跳过通用治理约束。

## 为什么（Why）
1. 前端可交互不代表链路可执行。
2. 无后端契约会导致界面行为和真实数据脱节。
3. 降级与审计缺失会扩大线上故障成本。
4. 强制并集可减少跨端返工和联调失败。

## 实操命令（项目级）

```bash
# 1) 锚点反查
rg -n "constraint_frontend_expansion_rule" references/anchor_docs/ANCHOR_DOC_REGISTRY.yaml references/anchor_docs/constraints

# 2) 图触发词检查
rg -n "trigger_any_of:.*frontend|ui|page|webapp|canvas|admin_ui" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 3) 扩展域并集检查
rg -n "frontend_domain|backend_domain|telegram_channel_domain|common_always_on" references/knowledge_graph/MOL_TECH_STACK_KEYWORD_ANCHOR_GRAPH_v1.md

# 4) 缺失阻断事件抽检
jq -c 'select(.status=="blocked" and .error_code=="missing_frontend_expansion_domain")' logs/*.jsonl | head

# 5) 前端输出主题完整性检查
rg -n "状态管理|接口契约|错误回执|权限可见性|降级" references/anchor_docs/frontend references/anchor_docs/common -S
```

## 最小验收
1. 前端关键词命中结果，`backend_domain` 附带率达到 100%。
2. Telegram WebApp 场景 `telegram_channel_domain` 附带率达到 100%。
3. 缺域或缺主题场景全部阻断，无放行记录。
4. 输出主题完整度覆盖率（5 项）达到 100%。
