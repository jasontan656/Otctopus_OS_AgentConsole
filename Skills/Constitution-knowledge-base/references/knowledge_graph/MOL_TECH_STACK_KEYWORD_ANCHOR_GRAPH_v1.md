# MOL_KEYWORD_ANCHOR_GRAPH_v1

## 1. 目标与输入

- 目标：把 `MOL_FULL_CANON.md` 中与工程实现相关、且适合静态检索和结构约束的语义锚点，整理为“可检索关键词图”。
- 输入基线：`assets/goal/MOL_FULL_CANON.md`
- 边界：本图只服务于仍由宪法库自身治理的可检索约束；已迁出的 Python、前端与项目结构规则不再由本图承接。
- 约束：检索只返回真实命中的约束锚点，不再强制附带已外移的通用结构/代码治理底座。

## 2. MOL 锚点提取（证据）

| anchor_id | MOL 证据 | 行号 |
|---|---|---:|
| `backend_thread_runtime` | Codex 从本机 WSL 交互迁移到项目后端线程运行时 | 54 |
| `telegram_chat_webapp_contract` | Telegram 作为试点入口，chat + WebApp 混合交互 | 85, 155 |
| `database_cache_tool_calls` | 阶段二要求 database + cache + 数据库读写工具 | 109 |
| `ops_audit_unified` | AI 代理动作与人工动作统一入日志并可审计 | 81, 91, 183 |
| `phase_gate_release` | 可用性/时延/成功率/会话隔离/审计追踪为门禁 | 66 |
| `admin_mobile_first_ui` | Admin UI 手机尺寸固定、桌面也维持竖屏布局 | 151 |
| `telegram_native_bridge` | Inline buttons / CallbackQuery / deep-link / sendDocument 等拼接能力 | 159 |
| `codex_devops_copilot` | Codex CLI 为开发+运维协作体，服从人类最高裁决 | 199 |

## 3. 关键词锚点图（Graph）

### 3.1 节点（含同义词）

```yaml
graph_nodes:
  common_always_on:
    keywords:
      - governance
      - constitution_binding
      - task_package
      - retrieval
      - query
      - expansion
      - cross_domain
      - handoff

  backend_domain:
    keywords:
      - backend
      - api
      - http_entry
      - route
      - handler
      - webhook
      - command
      - orchestration
      - worker
      - queue
      - task
      - session
      - thread_runtime
      - request
      - response
      - trace
      - idempotency
      - retry
      - dead_letter
      - payload
      - normalize

  database_domain:
    keywords:
      - database
      - persistence
      - storage
      - cache
      - session_store
      - migration
      - index
      - retention
      - replay
      - draft_state
      - idempotency_key
      - schema
      - contract

  codex_runtime_domain:
    keywords:
      - codex
      - runtime
      - exec
      - session
      - resume
      - reply
      - operator_channel
      - resident_process
      - daemon
      - thread
      - bridge
      - task_runner

  telegram_channel_domain:
    keywords:
      - telegram
      - bot
      - channel
      - webhook
      - update
      - callback
      - chat
      - message
      - receipt
      - start_parameter
      - deep_link
```

### 3.2 关系边（一次检索多域扩展）

```yaml
graph_edges:
  - from: telegram_channel_domain
    to: backend_domain
    reason: "渠道更新通常由后端入口接收、归一化与分发"

  - from: telegram_channel_domain
    to: database_domain
    reason: "消息回执、会话映射与持久化契约需可索引"

  - from: codex_runtime_domain
    to: backend_domain
    reason: "运行时调用与回包通常通过后端桥接"

  - from: codex_runtime_domain
    to: database_domain
    reason: "会话与执行结果需具备契约与结构约束"

  - from: backend_domain
    to: database_domain
    reason: "请求生命周期与状态持久化天然相关"

```

## 4. 召回与扩展规则（执行用）

```yaml
retrieval_policy:
  version: v1
  normalize:
    - lowercase
    - split_by_symbol
    - cn_en_alias_expand

  expansion_rules:
    - trigger_any_of: ["telegram", "channel", "webhook", "callback", "deep_link", "chat"]
      attach: ["telegram_channel_domain", "backend_domain", "database_domain"]

    - trigger_any_of: ["codex", "runtime", "session", "resume", "reply", "exec", "thread"]
      attach: ["codex_runtime_domain", "backend_domain", "database_domain"]

    - trigger_any_of: ["backend", "api", "worker", "queue", "request", "response", "payload", "normalize"]
      attach: ["backend_domain", "database_domain"]
```
