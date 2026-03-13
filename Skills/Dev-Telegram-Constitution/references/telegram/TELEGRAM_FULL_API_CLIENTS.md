---
doc_id: "dev_telegram_constitution.topic.full_api_clients"
doc_type: "topic_atom"
topic: "Telegram full API and custom client contract"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the full API line."
---

# Telegram Full API And Custom Clients Contract

## 能力范围
- 自定义 Telegram client
- 更底层 Telegram API 能力
- 非默认 Bot API 路线

## 默认裁决
- 如果目标只是开发“用户 interface / bot / mini app”，不走这条线。
- 只有在明确要做“自定义 Telegram 客户端”或需要更完整的 Telegram 对象能力时，才进入 Full API 路线。

## 官方硬约束
- 官方将 Bot API 与完整 Telegram API 明确区分；自定义 client 相关能力属于另一条开发面。[Telegram API](https://core.telegram.org/api)
- 不把 Full API 当 Bot API 的“增强版默认路径”；二者职责不同。[Telegram API](https://core.telegram.org/api)

## 社区落地共识
- Full API 路线的实现、风控、账号安全和兼容复杂度都显著更高，应单独立项。
- 若团队只是做产品入口或客服 bot，用 Full API 往往是过度设计。

## JSON 示例
- 说明：完整 Telegram API/TDLib/其他 client 库通常不是 Bot API 这种固定 JSON 回调面。下面给的是“客户端库归一化后的事件对象示例”，用于帮助 AI 理解这条线的数据复杂度，不应误认为 Bot API payload。
```json
{
  "@type": "updateNewMessage",
  "message": {
    "@type": "message",
    "id": 841239812349,
    "chat_id": -1002003004005,
    "date": 1773360700,
    "sender_id": {
      "@type": "messageSenderUser",
      "user_id": 123456789
    },
    "content": {
      "@type": "messageText",
      "text": {
        "@type": "formattedText",
        "text": "hello from a custom Telegram client"
      }
    }
  }
}
```

## 禁止项
- 不因为想“多拿一点能力”就默认改走 Full API。
- 不把 Full API 的风险和复杂度混入普通 Bot/Mini App 方案。
