---
doc_id: "dev_telegram_constitution.topic.bot_interface_practices"
doc_type: "topic_atom"
topic: "Telegram bot interface practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the bot interface line."
  - target: "TELEGRAM_DELIVERY_GUARDRAILS.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Bot interface choices should stay aligned with delivery guardrails."
---

# Telegram Bot Interface Practices

## 能力范围
- 私聊/群组/频道中的消息交互
- `/start`、`/help`、`/settings` 等全局命令
- Inline Keyboard、Reply Keyboard、callback_query
- Deep link 参数启动
- 群组里的 moderation / automation / assistant flows

## 默认裁决
- 如果流程可以用“1 到 3 次交互 + 少量按钮”完成，默认优先 Bot Interface。
- 如果流程是重表单、复杂筛选、多字段编辑，停止堆消息流，转 `Mini App`。

## 官方最佳实践
- 设置清晰的 `description/about/profile media`，让用户一眼知道 bot 做什么。[Bot Features](https://core.telegram.org/bots/features)
- 支持基础命令 `/start`、`/help`、`/settings`，让入口一致。[Bot Features](https://core.telegram.org/bots/features)
- 默认尊重群组 `Privacy Mode`，不要一上来就要求读取群内所有消息；只有确有必要再放开。[Bot Features](https://core.telegram.org/bots/features)
- Deep link 参数要短、稳定、可解析；官方建议参数仅使用允许字符，并推荐 base64url 编码二进制或特殊内容。[Bot Features](https://core.telegram.org/bots/features)

## 社区最佳实践
- 会话型 Bot 不要把完整状态机硬塞进 handler 分支；应显式设计 session / conversation 层。
- `callback_data` 只放短 token、短 key 或可逆 ID，不放大 JSON 负载。
- 菜单型交互要先做到“当前状态可重绘”，再追求复杂多层导航。
- 高峰期 Bot 不要把慢逻辑直接卡在 webhook 响应链里；先 ack，再异步继续。
  参考：grammY 对高负载和 webhook 超时的建议强调不要在 update 处理链里阻塞过久。[grammY Scaling Up](https://grammy.dev/advanced/scaling)

## JSON 示例
- 文本命令 update：
```json
{
  "update_id": 90010001,
  "message": {
    "message_id": 301,
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason",
      "username": "jason_demo",
      "language_code": "en"
    },
    "chat": {
      "id": 123456789,
      "type": "private",
      "first_name": "Jason",
      "username": "jason_demo"
    },
    "date": 1773360001,
    "text": "/start plan_telegram_ui",
    "entities": [
      {
        "offset": 0,
        "length": 6,
        "type": "bot_command"
      }
    ]
  }
}
```
- callback query update：
```json
{
  "update_id": 90010002,
  "callback_query": {
    "id": "4382bfdwdsb323b2",
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason",
      "username": "jason_demo",
      "language_code": "en"
    },
    "message": {
      "message_id": 302,
      "chat": {
        "id": 123456789,
        "type": "private"
      },
      "date": 1773360002,
      "text": "Choose deployment mode",
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "Webhook",
              "callback_data": "deploy:webhook"
            },
            {
              "text": "Polling",
              "callback_data": "deploy:polling"
            }
          ]
        ]
      }
    },
    "chat_instance": "239847234982734",
    "data": "deploy:webhook"
  }
}
```

## 不要做
- 不要把长表单、多步骤编辑、复杂购物流强行做成纯消息问答。
- 不要在群组里默认关闭隐私模式去读取所有消息，除非产品确实依赖它。
- 不要把消息文本当作唯一结构化输入；按钮、命令、短 token 才更稳。
