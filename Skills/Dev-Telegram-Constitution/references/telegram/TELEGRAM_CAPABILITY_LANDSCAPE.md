---
doc_id: "dev_telegram_constitution.index.capability_landscape"
doc_type: "index_doc"
topic: "Telegram capability landscape and routing index"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Capability questions should land here first."
  - target: "TELEGRAM_BOT_INTERFACE_PRACTICES.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Bot interface is the most common Telegram entry line."
  - target: "TELEGRAM_INLINE_MODE_PRACTICES.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Inline mode is a distinct Telegram interaction line."
  - target: "TELEGRAM_ATTACHMENT_MENU_PRACTICES.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Attachment menu is a distinct launch surface."
  - target: "TELEGRAM_MINI_APP_CONTRACT.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Mini Apps need a dedicated contract."
  - target: "TELEGRAM_PAYMENTS_AND_STARS.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Payments and Stars have separate compliance and UX rules."
  - target: "TELEGRAM_LOGIN_AND_IDENTITY.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Login and identity are a separate integration line."
  - target: "TELEGRAM_GAMES_AND_MEDIA.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Games and media features have distinct constraints."
  - target: "TELEGRAM_BUSINESS_INTEGRATION.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Business integration is a dedicated product line."
  - target: "TELEGRAM_FULL_API_CLIENTS.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Full Telegram API and custom clients are outside the default Bot API path."
---

# Telegram Capability Landscape

## 目标
- 把 Telegram 面向开发者的主线能力一次性列清，并给后续 AI 一个默认裁决入口。
- 先回答“这条需求属于哪条主线”，再进入具体合同文档。

## 主线能力总览
1. `Bot Interface`
   - 默认入口：命令、消息、按钮、回调、菜单、群组/频道交互
   - 默认文档：`TELEGRAM_BOT_INTERFACE_PRACTICES.md`
2. `Inline Mode`
   - 在任意聊天里通过 `@bot query` 触发内容/结果发送
   - 默认文档：`TELEGRAM_INLINE_MODE_PRACTICES.md`
3. `Attachment Menu`
   - 从附件菜单直接启动 Bot/Mini App
   - 默认文档：`TELEGRAM_ATTACHMENT_MENU_PRACTICES.md`
4. `Mini App / WebApp`
   - Telegram 内嵌富交互 UI
   - 默认文档：`TELEGRAM_MINI_APP_CONTRACT.md`
5. `Payments / Telegram Stars`
   - 数字商品、订阅、付费媒体、退款
   - 默认文档：`TELEGRAM_PAYMENTS_AND_STARS.md`
6. `Login / Identity`
   - Telegram 登录挂件、账号绑定
   - 默认文档：`TELEGRAM_LOGIN_AND_IDENTITY.md`
7. `Games / Media Extensions`
   - HTML5 游戏、高分、分享媒体、故事分享
   - 默认文档：`TELEGRAM_GAMES_AND_MEDIA.md`
8. `Business Integration`
   - Business 账号接入 bot 处理消息
   - 默认文档：`TELEGRAM_BUSINESS_INTEGRATION.md`
9. `Full Telegram API / Custom Clients`
   - 更底层 Telegram API、自定义客户端、非默认 Bot 路线
   - 默认文档：`TELEGRAM_FULL_API_CLIENTS.md`

## 默认裁决规则
- 只要目标是“做一个 Telegram 内的用户入口”，默认从 `Bot Interface`、`Inline Mode`、`Mini App` 三者中选。
- 只要需求涉及支付，必须额外读取 `Payments / Stars` 文档。
- 只要需求涉及身份登录或把 Telegram 账号接到站外系统，必须额外读取 `Login / Identity` 文档。
- 只要需求开始要求“像完整 Telegram 客户端一样控制更多对象”，默认视为 `Full API / Custom Clients`，不再沿用 Bot API 的默认路径。
- 未经显式立项，不进入 `Full Telegram API / Custom Clients`。

## 官方主源
- Bot Features: `https://core.telegram.org/bots/features`
- Bots Intro: `https://core.telegram.org/bots`
- Bot API: `https://core.telegram.org/bots/api`
- Inline Bots: `https://core.telegram.org/bots/inline`
- Mini Apps: `https://core.telegram.org/bots/webapps`
- Payments/Stars: `https://core.telegram.org/bots/payments-stars`
- Login Widget: `https://core.telegram.org/widgets/login`
- Telegram API: `https://core.telegram.org/api`
