---
doc_id: "dev_telegram_constitution.topic.login_and_identity"
doc_type: "topic_atom"
topic: "Telegram login and identity practices"
anchors:
  - target: "TELEGRAM_CAPABILITY_LANDSCAPE.md"
    relation: "implements"
    direction: "upstream"
    reason: "This doc elaborates the login and identity line."
  - target: "TELEGRAM_MINI_APP_CONTRACT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Identity and Mini App backend validation often work together."
---

# Telegram Login And Identity

## 能力范围
- Telegram Login Widget
- 用 bot 作为站外登录入口
- Telegram 用户与业务账户绑定

## 默认裁决
- 如果目标是“把 Telegram 账号接到站外系统”，优先 `Login Widget` 或 `Mini App init data + backend validation`。
- 如果只是在 bot 内部识别用户，不需要额外上站外登录挂件。

## 官方最佳实践
- Login Widget 需要一个 Telegram bot 承载。[Login Widget](https://core.telegram.org/widgets/login)
- 官方明确建议：用于授权的 bot 名称和头像应与站点品牌一致，降低用户疑惑感。[Login Widget](https://core.telegram.org/widgets/login)
- Mini App 身份不能只信前端传来的对象；官方 Mini App 文档要求把 `initData` 送到后端验证。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区最佳实践
- 账号绑定要区分“首次绑定”“重新绑定”“解绑/换绑”三个动作，不要只有一个模糊登录成功状态。
- 将 Telegram identity 与内部 account/session 分离，便于后续扩展其他登录方式。
- 身份成功后应落明确的后端 session，而不是持续依赖前端 query 参数。

## 不要做
- 不要只做前端校验，不做后端 `initData` 验证。
- 不要让品牌不一致的 bot 去承担登录入口。
