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
