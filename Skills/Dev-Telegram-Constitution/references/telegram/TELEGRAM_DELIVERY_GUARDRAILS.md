---
doc_id: "dev_telegram_constitution.topic.delivery_guardrails"
doc_type: "topic_atom"
topic: "Telegram delivery, callback, webhook, and safety guardrails"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends delivery and safety questions here."
  - target: "TELEGRAM_MINI_APP_CONTRACT.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Mini App delivery questions continue into the dedicated contract."
---

# Telegram Delivery Guardrails

## 本地目的
- 给 Telegram 作为用户入口时的消息流、回调、Webhook 和安全边界设定稳定规则。

## 当前边界
- 本文只描述 Telegram 侧交付与接口约束。
- 不替代具体业务状态机设计。

## 局部规则
- 生产环境走 `webhook`；本地调试或极轻量实验才走 `getUpdates`。
- 不把同一个 bot 的消息流设计成 `webhook` 和 `getUpdates` 双轨长期共存。
- Telegram update 一律视为外部不可信输入；进入业务逻辑前先做 normalize。
- 对 `callback_query` 必须设计快速响应路径，耗时工作放到后续异步处理。
- 任何会产生副作用的 Telegram 操作，都必须具备幂等键或去重策略。
- 消息编辑、删除、按钮点击和重试都可能重复到达，不能假设 Telegram 事件天然只来一次。
- 设计时显式记录 `chat_id/user_id/message_id/callback_query_id` 等关键映射字段。

## 交付裁决表
- `webhook`
  - 进入条件：生产入口、持续在线服务、可观测性要求更高的系统。
  - 强制要求：稳定 HTTPS、可回放日志、超时和重试边界。
- `getUpdates`
  - 进入条件：本地开发、一次性实验、小型工具。
  - 禁止进入：长期生产入口。
- `callback data`
  - 强制要求：保持短、稳定、可解析；不把大块业务 JSON 直接塞进按钮数据。
- `file/media`
  - 强制要求：由后端掌控下载、转存、扫描与大小策略，不把 Telegram 文件句柄直接当业务真值。
- `rate limit`
  - 强制要求：发送消息、编辑消息、批量通知都要考虑节流与失败退避。

## 社区落地共识
- `aiogram` 的 router/middleware 体系说明了“先过滤、再中间件、再 handler”的可分层事件处理模型，可把审计、鉴权、session 注入和风控从业务 handler 里拆出去。[aiogram Middlewares](https://docs.aiogram.dev/en/v3.13.1/dispatcher/middlewares.html)
- `grammY` 的部署文档明确提醒：webhook 处理链阻塞会导致 Telegram 重发未确认 update，高峰期应考虑队列、sequentialize/session key 一致性以及错误捕获。[grammY Deployment](https://grammy.dev/zh/advanced/deployment)

## JSON 示例
- `setWebhook` request body：
```json
{
  "url": "https://example.com/api/telegram/webhook",
  "secret_token": "tg_secret_9f2d6a84f0214e70",
  "allowed_updates": [
    "message",
    "callback_query",
    "inline_query",
    "pre_checkout_query",
    "business_connection",
    "business_message"
  ],
  "drop_pending_updates": false
}
```

## 安全边界
- Bot Token 必须放在受管密钥存储，不写进 repo。
- Mini App 的 init data 校验必须在服务端完成。
- 对外暴露的 webhook endpoint 必须具备来源校验、审计和错误观测字段。
- 不让 Telegram 文本、callback data 或 webapp_data 直接驱动敏感写操作。

## 例外与门禁
- 如果任务只是“如何写一个 bot handler”，本文不足以承接具体代码实现，应切到具体语言 skill。
- 如果任务是“如何设计 Mini App 与 Bot 协同”，必须继续读取 `TELEGRAM_MINI_APP_CONTRACT.md`。
