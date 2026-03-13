---
doc_id: "dev_telegram_constitution.topic.stack_baseline"
doc_type: "topic_atom"
topic: "Telegram stack and dependency baseline"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends framework and dependency questions here."
  - target: "TELEGRAM_DELIVERY_GUARDRAILS.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Stack choices should stay aligned with delivery mode."
---

# Telegram Stack Baseline

## 本地目的
- 给 Telegram interface 开发提供语言栈、框架与依赖的推荐基线。
- 避免每次都从零比较 Python / TypeScript / Mini App 组合。

## 当前边界
- 本文只回答“选什么栈更合适”，不替代具体代码实现。
- 版本与生态判断以当前公开官方文档为准；下列基线按 2026-03-13 核对过一次。

## 推荐栈矩阵
- `Python + Bot API + 常规业务 Bot`
  - 默认优先：`python-telegram-bot`
  - 当前公开 stable docs：`v22.6`
  - 适合：常规命令流、回调交互、Webhook/long polling、文档可读性优先的团队。
- `Python + asyncio + 明确事件路由 / 高并发 Bot`
  - 默认优先：`aiogram`
  - 当前公开 docs：`3.26.0`
  - 适合：router/middleware/filter 明确、异步边界清楚、吞吐要求更高的 Bot。
- `TypeScript / Node.js + Bot API`
  - 默认优先：`grammY`
  - 适合：TypeScript 优先、插件式能力组合、和前端/Node 工具链一致的团队。
- `TypeScript / Node.js + 历史项目`
  - 可延续：`Telegraf`
  - 适合：已有 Telegraf 资产或团队经验。
  - 不建议为新项目仅因历史知名度而优先于 `grammY`。
- `Telegram Mini App frontend`
  - 默认优先：`@telegram-apps/sdk` + `@telegram-apps/bridge`
  - 再叠加项目既有前端栈，例如 `Vue3 + TypeScript`。
  - UI 细节与组件系统仍由 `Dev-VUE3-WebUI-Frontend` 接管。

## 推荐辅助依赖
- `pydantic`
  - 用于 Telegram update、callback data、Mini App init data 派生 DTO 的显式结构化。
- `httpx`
  - Python 侧统一外部 HTTP 调用边界。
- `FastAPI` 或 `Starlette`
  - 当 Telegram webhook 需要和现有 HTTP 服务共栈时使用。
- `@grammyjs/*` 插件族
  - 在 `grammY` 路线下按需补 session、menu、conversations 等能力。

## 选型规则
- 新项目若以 Python 为主、可读性优先，默认先选 `python-telegram-bot`。
- 新项目若以 TypeScript 为主，默认先选 `grammY`，除非团队已有稳定 `Telegraf` 存量。
- 若 Telegram 只是一个渠道，而核心系统仍在 Python 服务内，不要为了 Telegram 单独把整个后端改成 Node。
- Mini App frontend 栈应跟项目主前端栈对齐，不要为了 Telegram 容器单独再造第二套前端规范。

## 当前主源
- Telegram Bot API: `https://core.telegram.org/bots/api`
- Telegram Mini Apps: `https://docs.telegram-mini-apps.com/`
- python-telegram-bot stable docs: `https://docs.python-telegram-bot.org/en/stable/`
- aiogram docs: `https://docs.aiogram.dev/en/latest/`
- grammY docs: `https://grammy.dev/`
- Telegraf docs: `https://telegraf.js.org/`

## 例外与门禁
- 若任务涉及用户账号自动化而非 Bot API，默认视为超出本技能主路径，需要单独说明风险与边界。
- 若任务开始进入 Python 代码写法、类型设计或 lint 执行，转入 `Dev-PythonCode-Constitution`。
