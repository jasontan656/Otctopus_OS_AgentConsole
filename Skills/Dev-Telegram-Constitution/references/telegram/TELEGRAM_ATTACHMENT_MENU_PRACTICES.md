---
doc_id: dev_telegram_constitution.topic.attachment_menu_practices
doc_type: topic_atom
topic: Telegram attachment menu decision contract
anchors:
- target: TELEGRAM_CAPABILITY_LANDSCAPE.md
  relation: implements
  direction: upstream
  reason: This doc elaborates the attachment menu line.
- target: TELEGRAM_MINI_APP_RULES.md
  relation: pairs_with
  direction: lateral
  reason: Attachment menu often launches Mini Apps.
---

# Telegram Attachment Menu Contract

## 能力范围
- 从附件菜单直接启动 bot 的 Mini App
- 配置可在哪些聊天类型中启动
- 为 Mini App 提供更稳定、更高频的入口

## 默认裁决
- 如果产品需要“用户在任何聊天都能快速拉起”，Attachment Menu 作为强入口纳入方案。
- 如果产品只是一次性或低频流程，先做普通 Bot / Deep Link，不为附件菜单提前引入复杂度。

## 官方硬约束
- Attachment Menu 不是所有 bot 默认都有的普遍入口；官方文档说明它目前仍有准入限制，测试环境可先验证。[Mini Apps](https://core.telegram.org/bots/webapps)
- 必须明确允许启动的聊天类型（private / groups / supergroups / channels）。[Mini Apps](https://core.telegram.org/bots/webapps)
- 如使用 Settings 菜单项，必须处理 `settingsButtonClicked` 事件。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区落地共识
- 把附件菜单视为“常驻产品入口”，常见落点是客服工具、商家工具、内容面板、常用控制台。
- 如果入口很多，启动后直接落到用户最常用任务，而不是只打开 landing page。

## JSON 示例
- `setChatMenuButton` body：
```json
{
  "chat_id": 123456789,
  "menu_button": {
    "type": "web_app",
    "text": "Open Console",
    "web_app": {
      "url": "https://example.com/tg/app/main"
    }
  }
}
```

## 禁止项
- 不把附件菜单当唯一入口。
- 不假设所有正式 bot 都能直接获得该入口能力。
