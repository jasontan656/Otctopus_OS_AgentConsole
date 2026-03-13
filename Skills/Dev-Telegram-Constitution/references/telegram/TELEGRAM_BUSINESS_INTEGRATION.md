---
doc_id: "dev_telegram_constitution.topic.business_integration"
doc_type: "topic_atom"
topic: "Telegram Business integration practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the business integration line."
---

# Telegram Business Integration

## 能力范围
- Business 用户把 bot 接入为消息处理者
- 企业服务、客服、消息自动化

## 默认裁决
- 如果产品目标是“企业客服 / 商家服务 / 业务自动回复”，优先评估 Business integration。
- 如果只是普通个人 bot，不要把 Business 相关复杂度提前引入。

## 官方最佳实践
- Telegram 官方 bots 入口已将 Business 作为 bot 的一条正式集成主线。[Bots Intro](https://core.telegram.org/bots)
- Business 接入应围绕“代表业务身份处理消息”设计，而不是把普通 bot 聊天逻辑原样硬套过去。[Bots Intro](https://core.telegram.org/bots)

## 社区最佳实践
- Business 接入场景要特别重视权限、审计、人工接管和 SLA。
- 自动回复、工单状态、人工转接应拆成不同责任面，不要所有消息都交给一个 giant handler。

## JSON 示例
- business connection update：
```json
{
  "update_id": 90015001,
  "business_connection": {
    "id": "bc_8d1d7ab1",
    "user": {
      "id": 555000111,
      "is_bot": false,
      "first_name": "Merchant",
      "username": "merchant_owner"
    },
    "user_chat_id": 555000111,
    "date": 1773360600,
    "can_reply": true,
    "is_enabled": true
  }
}
```
- business message update：
```json
{
  "update_id": 90015002,
  "business_message": {
    "message_id": 710,
    "business_connection_id": "bc_8d1d7ab1",
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Customer",
      "username": "customer_one"
    },
    "chat": {
      "id": 555000111,
      "type": "private"
    },
    "date": 1773360605,
    "text": "I need help with my order #A-1007"
  }
}
```

## 不要做
- 不要把企业客服流程设计成“只能 bot 回复、没有人工兜底”。
- 不要缺少消息归属、转接和审计字段。
