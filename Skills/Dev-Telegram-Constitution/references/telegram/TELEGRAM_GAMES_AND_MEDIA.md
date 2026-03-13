---
doc_id: "dev_telegram_constitution.topic.games_and_media"
doc_type: "topic_atom"
topic: "Telegram games and media practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the games and media line."
---

# Telegram Games And Media

## 能力范围
- HTML5 Games
- 游戏高分
- 分享媒体、分享至故事
- Mini App 生成媒体后分享

## 默认裁决
- 如果需求是“轻量游戏 + 排行榜 + 分享”，优先 Telegram Games / Mini App。
- 如果需求是重度实时游戏引擎或高度自定义客户端体验，Telegram 只适合作为分发和承载面，不应强行当原生游戏平台。

## 官方最佳实践
- 游戏可通过 bot 发起，并通过 `answerCallbackQuery` 的 URL 启动 HTML5 游戏。[Bot Features](https://core.telegram.org/bots/features)
- 高分应走 `setGameScore` / `getGameHighScores` 等官方路径。[Bot Features](https://core.telegram.org/bots/features)
- Mini App 可分享媒体，也可通过 `shareToStory` 等方式进入 Telegram Stories。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区最佳实践
- 游戏分数、奖励、排行榜都应以后端为真值，不要只信前端上报。
- 适合把“分享战绩/生成卡片/邀请链接”设计成传播环节，而不是把复杂社交关系全压到 Telegram UI 上。

## JSON 示例
- `sendGame` request body：
```json
{
  "chat_id": 123456789,
  "game_short_name": "octopus_runner",
  "reply_markup": {
    "inline_keyboard": [
      [
        {
          "text": "Play",
          "callback_game": {}
        }
      ],
      [
        {
          "text": "Leaderboard",
          "callback_data": "game:leaderboard:octopus_runner"
        }
      ]
    ]
  }
}
```
- game launch callback：
```json
{
  "update_id": 90014001,
  "callback_query": {
    "id": "game_cb_001",
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason"
    },
    "message": {
      "message_id": 610,
      "chat": {
        "id": 123456789,
        "type": "private"
      },
      "date": 1773360500,
      "game": {
        "title": "Octopus Runner",
        "description": "A lightweight Telegram HTML5 game",
        "photo": [
          {
            "file_id": "AgACAgUAAxkBAAIBQmY",
            "file_unique_id": "AQAD1e8xG2",
            "width": 512,
            "height": 512
          }
        ]
      }
    },
    "chat_instance": "987654321012345678",
    "game_short_name": "octopus_runner"
  }
}
```

## 不要做
- 不要把客户端可篡改分数直接写入排行榜。
- 不要假设游戏运行环境等同标准浏览器环境。
