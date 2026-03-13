---
doc_id: "dev_telegram_constitution.topic.payments_and_stars"
doc_type: "topic_atom"
topic: "Telegram payments and Stars contract"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the payments and Stars line."
---

# Telegram Payments And Stars Contract

## 能力范围
- 数字商品和服务支付
- 订阅、付费媒体、退款
- 内联发票

## 默认裁决
- 只要商品属于“数字商品/数字服务”，在 Telegram app 内成交时走 `Telegram Stars`。
- 如果是实物商品或线下服务，再单独评估其他支付提供方。

## 官方硬约束
- 数字商品和服务在 Telegram app 内支付，必须用 `Telegram Stars`，不能绕第三方支付。[Payments/Stars](https://core.telegram.org/bots/payments-stars)
- bot 或 Mini App 都可以发起数字商品支付，但仍需要 bot 作为支付承载面。[Payments/Stars](https://core.telegram.org/bots/payments-stars)
- 必须实现 `/paysupport`，并能处理支付争议和用户支持请求。[Payments/Stars](https://core.telegram.org/bots/payments-stars)
- 退款走 `refundStarPayment` 等官方路径，不自造“账外口头退款”流程。[Payments/Stars](https://core.telegram.org/bots/payments-stars)

## 社区落地共识
- 付款前先把商品说明、计费周期、退款语义说清楚，避免在 Telegram 聊天上下文里造成误购。
- 把支付成功、失败、退款、订阅续期都做成独立可审计事件，不只依赖客户端提示。
- 对付费媒体和订阅，采用“支付后即时回执 + 后端异步履约”。

## JSON 示例
- `sendInvoice` for Stars：
```json
{
  "chat_id": 123456789,
  "title": "Pro Subscription",
  "description": "30-day access to premium Telegram workflow features",
  "payload": "sub_30d_user_123456789_plan_pro",
  "currency": "XTR",
  "prices": [
    {
      "label": "30-day Pro plan",
      "amount": 250
    }
  ]
}
```
- incoming `pre_checkout_query` update：
```json
{
  "update_id": 90013001,
  "pre_checkout_query": {
    "id": "129384712938471",
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason",
      "username": "jason_demo"
    },
    "currency": "XTR",
    "total_amount": 250,
    "invoice_payload": "sub_30d_user_123456789_plan_pro"
  }
}
```
- successful payment message：
```json
{
  "update_id": 90013002,
  "message": {
    "message_id": 520,
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason"
    },
    "chat": {
      "id": 123456789,
      "type": "private"
    },
    "date": 1773360300,
    "successful_payment": {
      "currency": "XTR",
      "total_amount": 250,
      "invoice_payload": "sub_30d_user_123456789_plan_pro",
      "telegram_payment_charge_id": "528463847264",
      "provider_payment_charge_id": "tg_stars_internal"
    }
  }
}
```

## 禁止项
- 不在数字商品场景继续采用第三方币种或外链支付作为 Telegram 内主路径。
- 不缺 `/paysupport`。
- 不把支付成功提示当成唯一真值，后端仍要做订单状态确认。
