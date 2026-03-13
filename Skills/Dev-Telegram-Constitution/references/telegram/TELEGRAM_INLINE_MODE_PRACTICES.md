---
doc_id: "dev_telegram_constitution.topic.inline_mode_practices"
doc_type: "topic_atom"
topic: "Telegram inline mode practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the inline mode line."
---

# Telegram Inline Mode Practices

## 能力范围
- 在任意聊天中通过 `@bot query` 触发结果
- 可返回多种 Telegram 内容类型
- 可通过 `switch to PM` 在 inline 与私聊之间切换
- 可选位置权限以返回地理相关结果

## 默认裁决
- 如果你的产品价值是“让用户把内容带到任意聊天里分享”，优先 Inline Mode。
- 如果价值在复杂配置、账号连接或多步骤输入，Inline 只做分发入口，主流程仍应回 Bot 私聊或 Mini App。

## 官方最佳实践
- Inline 能力必须在 `@BotFather` 显式开启，否则收不到 inline updates。[Inline Bots](https://core.telegram.org/bots/inline)
- Inline 结果应围绕“快速搜索、快速发送”设计，而不是把它当复杂应用面。[Inline Bots](https://core.telegram.org/bots/inline)
- 需要用户先完成配置时，应使用 `Switch to PM` 把用户带回私聊完成 setup，再跳回 inline 发送。[Inline Bots](https://core.telegram.org/bots/inline)
- 位置敏感结果应显式开启 inline geo，而不是私自假定位置可用。[Inline Bots](https://core.telegram.org/bots/inline)

## 社区最佳实践
- Inline 查询返回要足够快，否则用户体验会迅速崩掉；应尽量做缓存与预计算。
- 结果卡片文案要短，因为用户是在聊天输入框上下文里快速做选择。
- 如果结果依赖第三方账号连接，默认给出“先授权再返回结果”的引导，不要静默空结果。

## 不要做
- 不要把 inline 当成完整管理后台。
- 不要把必须长时间编辑的内容塞进 inline 结果选择。
- 不要在 inline query 上直接做重计算和慢 I/O。
