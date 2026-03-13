---
doc_id: "dev_telegram_constitution.topic.attachment_menu_practices"
doc_type: "topic_atom"
topic: "Telegram attachment menu practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the attachment menu line."
  - target: "TELEGRAM_MINI_APP_CONTRACT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Attachment menu often launches Mini Apps."
---

# Telegram Attachment Menu Practices

## 能力范围
- 从附件菜单直接启动 bot 的 Mini App
- 配置可在哪些聊天类型中启动
- 可为 Mini App 提供更稳定、更高频的入口

## 默认裁决
- 如果产品需要“用户在任何聊天都能快速拉起”，Attachment Menu 是强入口。
- 如果产品只是一次性或低频流程，先做普通 Bot / Deep Link，不必默认追求附件菜单。

## 官方最佳实践
- Attachment Menu 不是所有 bot 默认都有的普遍入口；官方文档说明它目前仍有准入限制，测试环境可先验证。[Mini Apps](https://core.telegram.org/bots/webapps)
- 应明确允许启动的聊天类型（private / groups / supergroups / channels）。[Mini Apps](https://core.telegram.org/bots/webapps)
- 如使用 Settings 菜单项，应处理 `settingsButtonClicked` 事件。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区最佳实践
- 把附件菜单视为“常驻产品入口”，适合客服工具、商家工具、内容面板、常用控制台。
- 如果入口很多，先保证启动后就能落到用户最常用任务，而不是只打开 landing page。

## 不要做
- 不要把附件菜单当唯一入口。
- 不要假设所有正式 bot 都能直接获得该入口能力。
