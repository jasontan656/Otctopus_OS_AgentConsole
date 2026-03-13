---
doc_id: "dev_telegram_constitution.topic.inline_mode_practices"
doc_type: "topic_atom"
topic: "Telegram inline mode decision contract"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the inline mode line."
---

# Telegram Inline Mode Contract

## 能力范围
- 在任意聊天中通过 `@bot query` 触发结果
- 可返回多种 Telegram 内容类型
- 可通过 `switch to PM` 在 inline 与私聊之间切换
- 可选位置权限以返回地理相关结果

## 默认裁决
- 如果产品价值是“让用户把内容带到任意聊天里分享”，落 Inline Mode。
- 如果价值在复杂配置、账号连接或多步骤输入，Inline 只做分发入口，主流程回 Bot 私聊或 Mini App。

## 官方硬约束
- Inline 能力必须在 `@BotFather` 显式开启，否则收不到 inline updates。[Inline Bots](https://core.telegram.org/bots/inline)
- Inline 结果围绕“快速搜索、快速发送”设计，不把它当复杂应用面。[Inline Bots](https://core.telegram.org/bots/inline)
- 需要用户先完成配置时，使用 `Switch to PM` 把用户带回私聊完成 setup，再跳回 inline 发送。[Inline Bots](https://core.telegram.org/bots/inline)
- 位置敏感结果显式开启 inline geo，不私自假定位置可用。[Inline Bots](https://core.telegram.org/bots/inline)

## 社区落地共识
- Inline 查询返回必须足够快；慢查询要做缓存与预计算。
- 结果卡片文案保持短，因为用户是在聊天输入框上下文里快速做选择。
- 如果结果依赖第三方账号连接，给出“先授权再返回结果”的引导，不返回静默空结果。

## JSON 示例
- incoming inline query update：
```json
{
  "update_id": 90011001,
  "inline_query": {
    "id": "AAHdF6IQAAAAAN0XohDhrOrc",
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason",
      "username": "jason_demo",
      "language_code": "en"
    },
    "query": "deploy checklist",
    "offset": "",
    "chat_type": "sender"
  }
}
```
- `answerInlineQuery` request body：
```json
{
  "inline_query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
  "cache_time": 30,
  "is_personal": true,
  "results": [
    {
      "type": "article",
      "id": "deploy_checklist_v1",
      "title": "Deployment Checklist",
      "description": "Send a deployment checklist to the current chat",
      "input_message_content": {
        "message_text": "Deployment checklist:\n1. confirm webhook secret\n2. verify Redis session store\n3. run smoke test"
      },
      "reply_markup": {
        "inline_keyboard": [
          [
            {
              "text": "Open Mini App",
              "web_app": {
                "url": "https://example.com/tg/app/checklist"
              }
            }
          ]
        ]
      }
    }
  ],
  "button": {
    "text": "Switch to Mini App",
    "web_app": {
      "url": "https://example.com/tg/app/inline-builder"
    }
  }
}
```

## 禁止项
- 不把 inline 当成完整管理后台。
- 不把必须长时间编辑的内容塞进 inline 结果选择。
- 不在 inline query 上直接做重计算和慢 I/O。
