---
doc_id: "dev_telegram_constitution.topic.stack_baseline"
doc_type: "topic_atom"
topic: "Telegram stack decision contract and dependency state"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends framework and dependency questions here."
  - target: "TELEGRAM_DELIVERY_GUARDRAILS.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Stack choices should stay aligned with delivery mode."
---

# Telegram Stack Decision Contract

## 本地目的
- 给 Telegram interface 开发提供语言栈、框架与依赖的裁决状态。
- 避免每次都把候选依赖误写成既定选型。

## 当前边界
- 本文只回答“哪些栈已经定版、哪些仍待用户裁决”，不替代具体代码实现。
- 版本与生态判断以当前公开官方文档为准；下列状态按 2026-03-13 核对过一次。

## 当前选型状态
- `Telegram Bot API`：已裁决为默认主路径。
- `用户账号自动化 / MTProto / Full API`：未单独立项时禁止默认进入。
- `Mini App frontend bridge`：已裁决为 `@telegram-apps/sdk` + `@telegram-apps/bridge`。
- `Python Bot 主实现栈`：待用户裁决。
- `TypeScript Bot 主实现栈`：待用户裁决。

## Python 候选裁决集
- 方案 A `PTB 主线`
  - 排序：第一候选。
  - 组件：`python-telegram-bot[webhooks,rate-limiter,job-queue,callback-data]`、`FastAPI`、`pydantic`、`httpx`、`orjson`。
  - 进入条件：常规命令流、回调交互、Inline、Payments、Webhook/long polling、以文档可读性作为第一约束。
  - 不进入条件：项目明确要求以 router/middleware/FSM 为主组织事件层，且高并发异步边界是第一约束。
  - 说明：`python-telegram-bot` 当前官方 stable docs 为 `v22.6`，默认 networking backend 依赖 `httpx`，并提供 `AIORateLimiter`、`JobQueue` 等官方扩展入口。
- 方案 B `aiogram 主线`
  - 排序：第二候选。
  - 组件：`aiogram`、`FastAPI`、`redis`、`pydantic`、`httpx`、`orjson`。
  - 进入条件：asyncio-first、router/middleware/filter/FSM 分层是第一约束，且需要更强的事件管线控制。
  - 不进入条件：团队更看重文档可读性、PTB 生态例子、较低的认知门槛。
  - 说明：`aiogram` 当前公开 docs 可核到 `3.22.0`；其 3.x 线强调 router、middleware、flags、FSM storage 和 pydantic validation。
- 方案 C `自写 Bot API wrapper`
  - 状态：禁止默认采用。
  - 禁止理由：重复造轮子，且会失去成熟生态对 update type、Bot API 兼容、rate limit 与支付能力的维护。

## 固定辅助依赖裁决
- `pydantic`
  - 状态：已裁决。
  - 用途：对 Telegram update、callback data、Mini App init data 派生 DTO 做显式结构化。
- `httpx`
  - 状态：已裁决。
  - 用途：统一 Python 侧外部 HTTP 调用边界；PTB 默认 networking backend 也依赖它。
- `FastAPI`
  - 状态：第一候选。
  - 用途：Webhook 与现有 HTTP 服务共栈时的首选承载层。
- `Starlette`
  - 状态：备选。
  - 用途：仅在需要极薄 ASGI 层且团队已熟悉时采用。
- `orjson`
  - 状态：已裁决为生产增强依赖。
  - 用途：大量 update/webhook 解析和日志落盘。
- `redis`
  - 状态：条件性依赖。
  - 进入条件：需要分布式 session、FSM storage、异步队列协同时启用。

## 选型规则
- 在用户没有定版前，AI 只能引用候选方案，不得直接写死 `python-telegram-bot` 或 `aiogram` 代码。
- 若项目主后端是 Python，Telegram 作为渠道接入时，不为了渠道单独把主后端改成 Node。
- Mini App frontend 栈必须跟项目主前端栈对齐，不为 Telegram 容器额外造第二套前端规范。
- TypeScript Bot 路线待用户裁决；在没有明确要求前，不主动把主实现栈切到 Node。

## AI 执行门禁
- 若任务是“先定规范再开发”，而 `Python Bot 主实现栈` 仍未裁决，AI 必须先返回候选方案差异，不得直接产出框架实现代码。
- 若用户明确指定 `python-telegram-bot` 或 `aiogram`，从该刻起视为已裁决，可在后续任务中按该栈执行。
- 若用户只说“Python 做 Telegram”，当前默认先向用户主推方案 A，再等待用户定版。

## 当前主源
- Telegram Bot API: `https://core.telegram.org/bots/api`
- Telegram Mini Apps: `https://docs.telegram-mini-apps.com/`
- python-telegram-bot stable docs: `https://docs.python-telegram-bot.org/en/stable/`
- aiogram docs: `https://docs.aiogram.dev/en/latest/`
- grammY docs: `https://grammy.dev/`
- Telegraf docs: `https://telegraf.js.org/`

## Python 组合包候选
- `候选 A：PTB 生产 webhook Bot`
```text
python-telegram-bot[webhooks,rate-limiter,job-queue,callback-data]
FastAPI
pydantic
httpx
orjson
```
- `候选 B：aiogram 高并发 Bot`
```text
aiogram
FastAPI
redis
pydantic
httpx
orjson
```
- `候选 C：Mini App 配套 Python 后端`
```text
FastAPI
python-telegram-bot or aiogram
pydantic
httpx
orjson
```

## 例外与门禁
- 若任务涉及用户账号自动化而非 Bot API，默认视为超出本技能主路径，需要单独说明风险与边界。
- 若任务开始进入 Python 代码写法、类型设计或 lint 执行，转入 `Dev-PythonCode-Constitution`。
