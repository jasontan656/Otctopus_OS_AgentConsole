---
doc_id: dev_telegram_constitution.topic.login_and_identity
doc_type: topic_atom
topic: Telegram login and identity contract
anchors:
- target: TELEGRAM_CAPABILITY_LANDSCAPE.md
  relation: implements
  direction: upstream
  reason: This doc elaborates the login and identity line.
- target: TELEGRAM_MINI_APP_RULES.md
  relation: pairs_with
  direction: lateral
  reason: Identity and Mini App backend validation often work together.
---

# Telegram Login And Identity Contract

## 能力范围
- Telegram Login Widget
- 用 bot 作为站外登录入口
- Telegram 用户与业务账户绑定

## 默认裁决
- 如果目标是“把 Telegram 账号接到站外系统”，落 `Login Widget` 或 `Mini App init data + backend validation`。
- 如果只是在 bot 内部识别用户，不上站外登录挂件。

## 官方硬约束
- Login Widget 需要一个 Telegram bot 承载。[Login Widget](https://core.telegram.org/widgets/login)
- 用于授权的 bot 名称和头像应与站点品牌一致，降低用户疑惑感。[Login Widget](https://core.telegram.org/widgets/login)
- Mini App 身份不能只信前端传来的对象；官方 Mini App 文档要求把 `initData` 送到后端验证。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区落地共识
- 账号绑定区分“首次绑定”“重新绑定”“解绑/换绑”三个动作，不保留一个模糊登录成功状态。
- Telegram identity 与内部 account/session 分离，便于后续扩展其他登录方式。
- 身份成功后落明确的后端 session，不持续依赖前端 query 参数。

## JSON 示例
- `login_url` button config：
```json
{
  "reply_markup": {
    "inline_keyboard": [
      [
        {
          "text": "Login with Telegram",
          "login_url": {
            "url": "https://example.com/auth/telegram/callback",
            "forward_text": "Login to Example",
            "bot_username": "example_auth_bot",
            "request_write_access": true
          }
        }
      ]
    ]
  }
}
```
- 登录回调归一化对象：
```json
{
  "id": 123456789,
  "first_name": "Jason",
  "last_name": "Tan",
  "username": "jason_demo",
  "photo_url": "https://t.me/i/userpic/320/jason_demo.jpg",
  "auth_date": 1773360400,
  "hash": "8e6a7d9b9f47e4a34fba8df00a17af8e4bfa2c2d0fb5a8d67be93175b6c6a112"
}
```

## 禁止项
- 不只做前端校验，不做后端 `initData` 验证。
- 不让品牌不一致的 bot 承担登录入口。
