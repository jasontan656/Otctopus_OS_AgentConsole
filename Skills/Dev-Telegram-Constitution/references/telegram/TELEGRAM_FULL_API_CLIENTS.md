---
doc_id: "dev_telegram_constitution.topic.full_api_clients"
doc_type: "topic_atom"
topic: "Telegram full API and custom client practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the full API line."
---

# Telegram Full API And Custom Clients

## 能力范围
- 自定义 Telegram client
- 更底层 Telegram API 能力
- 非默认 Bot API 路线

## 默认裁决
- 如果你的目标只是开发“用户 interface / bot / mini app”，不要走这条线。
- 只有在你明确要做“自定义 Telegram 客户端”或需要更完整的 Telegram 对象能力时，才进入 Full API 路线。

## 官方最佳实践
- 官方将 Bot API 与完整 Telegram API 明确区分；自定义 client 相关能力属于另一条开发面。[Telegram API](https://core.telegram.org/api)
- 不应把 Full API 当 Bot API 的“增强版默认路径”；二者职责不同。[Telegram API](https://core.telegram.org/api)

## 社区最佳实践
- Full API 路线的实现、风控、账号安全和兼容复杂度都显著更高，应单独立项。
- 若团队只是做产品入口或客服 bot，用 Full API 往往是过度设计。

## 不要做
- 不要因为想“多拿一点能力”就默认改走 Full API。
- 不要把 Full API 的风险和复杂度混入普通 Bot/Mini App 方案。
