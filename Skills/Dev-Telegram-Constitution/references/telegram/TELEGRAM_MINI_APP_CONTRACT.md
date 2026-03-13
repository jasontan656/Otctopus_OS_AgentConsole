---
doc_id: "dev_telegram_constitution.topic.mini_app_contract"
doc_type: "topic_atom"
topic: "Telegram Mini App contract and boundary"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends Mini App questions here."
  - target: "TELEGRAM_INTERFACE_SURFACES.md"
    relation: "implements"
    direction: "upstream"
    reason: "Mini App is one of the Telegram interface surfaces."
---

# Telegram Mini App Contract

## 本地目的
- 约束 Telegram Mini App 不被错误当成“普通 H5 页面”。
- 让 Telegram 容器、前端页面、后端会话和身份验证边界一次性说清楚。

## 当前边界
- 本文只治理 Mini App 与 Telegram 容器的合同。
- 前端组件系统与页面设计细节仍由 `Dev-VUE3-WebUI-Frontend` 接管。

## 核心合同
- Mini App frontend 只是 Telegram 容器中的交互投影，不是业务真值层。
- 用户身份、权限、写操作边界和订单/任务状态必须由后端判定。
- `init data` 必须在服务端验证，不能只在前端信任 Telegram 注入值。
- Mini App 内产生的业务动作，必须和后端 session / token / state machine 对齐。

## 推荐技术栈
- 容器桥接：`@telegram-apps/sdk` + `@telegram-apps/bridge`
- 前端：沿用项目主前端栈，例如 `Vue3 + TypeScript`
- 后端：继续使用项目主服务栈，不为 Mini App 单独发明一套后端框架

## 官方最佳实践
- 把 `Telegram.WebApp.initData` 送到 bot/backend 验证，而不是只在前端使用。[Mini Apps](https://core.telegram.org/bots/webapps)
- 主 Mini App、直达 `startapp` 链接、Inline 中 `Switch to Mini App` 都是官方支持的入口，需要按产品目标选择。[Mini Apps](https://core.telegram.org/bots/webapps)
- 可通过 `@BotFather` 配置 loading screen、main Mini App 等容器层能力。[Mini Apps](https://core.telegram.org/bots/webapps)

## 社区最佳实践
- 先规划用户路径，再接 SDK；常见顺序是：定义 flow -> 接 BotFather -> 做移动端 UI -> 接 SDK -> 做后端验证 -> 真机测试。
  参考：telegram-mini-app.dev 的 Mini App guide 总结了这一套落地顺序。[Community Guide](https://www.telegram-mini-app.dev/blog/telegram-mini-app-guide)
- 使用 Telegram 容器的 back button、safe area、viewport、theme，避免做成“看起来像普通网页但在 Telegram 里很别扭”的 UI。[Community Guide](https://www.telegram-mini-app.dev/blog/telegram-mini-app-guide)

## JSON 示例
- `web_app_data` update：
```json
{
  "update_id": 90012001,
  "message": {
    "message_id": 410,
    "from": {
      "id": 123456789,
      "is_bot": false,
      "first_name": "Jason",
      "username": "jason_demo",
      "language_code": "en"
    },
    "chat": {
      "id": 123456789,
      "type": "private"
    },
    "date": 1773360200,
    "web_app_data": {
      "button_text": "Open Scheduler",
      "data": "{\"action\":\"submit_schedule\",\"draft_id\":\"draft_42\",\"timezone\":\"Asia/Shanghai\",\"slots\":[\"2026-03-14T09:00:00+08:00\"]}"
    }
  }
}
```
- 前端可见 `initDataUnsafe` 归一化示例：
```json
{
  "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
  "user": {
    "id": 123456789,
    "is_bot": false,
    "first_name": "Jason",
    "last_name": "Tan",
    "username": "jason_demo",
    "language_code": "en",
    "allows_write_to_pm": true
  },
  "auth_date": 1773360200,
  "start_param": "main_dashboard",
  "chat_type": "sender",
  "chat_instance": "239847234982734",
  "hash": "e8d7f6e9c9f42f5b7a9e5f4d4b2e9ad0a8a5f7cb6e7a9b2d8e8c1f0b7d0f9c12"
}
```
- `answerWebAppQuery` request body：
```json
{
  "web_app_query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
  "result": {
    "type": "article",
    "id": "draft_saved_42",
    "title": "Draft saved",
    "input_message_content": {
      "message_text": "Draft #42 saved from Mini App."
    }
  }
}
```

## 局部规则
- Mini App 页面应假设用户主要在移动端内打开。
- 任何需要长时间编辑、复杂筛选和多字段输入的流程，都优先在 Mini App 完成，而不是消息流硬拼。
- Mini App 与 Bot 消息流应有明确分工：
  - Bot：提醒、入口、确认、轻操作
  - Mini App：复杂表单、富展示、批量编辑、面板式交互
- Mini App 退出、刷新、网络抖动后必须能恢复关键上下文，不能把关键状态只放在前端内存里。

## 例外与门禁
- 如果一个需求完全可以用 `Inline Keyboard + callback_query` 完成，就不要强行上 Mini App。
- 如果任务开始讨论具体页面组件、布局、动效和 design system，切到 `Dev-VUE3-WebUI-Frontend`。
