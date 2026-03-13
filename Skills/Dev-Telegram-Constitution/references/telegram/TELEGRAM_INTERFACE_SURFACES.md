---
doc_id: dev_telegram_constitution.topic.interface_surfaces
doc_type: topic_atom
topic: Telegram interface surfaces and capability decision contract
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends Telegram capability questions here.
- target: TELEGRAM_CAPABILITY_LANDSCAPE.md
  relation: implements
  direction: upstream
  reason: Capability landscape should be read before surface selection.
- target: TELEGRAM_STACK_BASELINE.md
  relation: pairs_with
  direction: lateral
  reason: Capability choice and stack choice should be read together.
- target: TELEGRAM_MINI_APP_RULES.md
  relation: routes_to
  direction: downstream
  reason: Mini App questions should continue into the dedicated contract.
---

# Telegram Interface Surface Contract

## 本地目的
- 让模型先判断 Telegram 需求应该落在哪一种交互面，再讨论实现。
- 避免把所有需求都粗暴落成“发消息 + 收命令”的单一 Bot 方案。

## 主线前置
- 更高层的主线能力划分先见 `TELEGRAM_CAPABILITY_LANDSCAPE.md`。
- 本文只负责在 Bot / Inline / Deep Link / Login / Mini App 这些典型用户入口面之间做选择。

## 当前边界
- 本文只负责 Telegram 能力分层与交互面裁决。
- 不负责具体框架 API 写法。
- 不负责前端组件细节与系统级目录落点。

## 交互面裁决表
1. `Bot command / plain message`
   - 进入条件：轻量命令、FAQ、状态查询、通知确认。
   - 裁决理由：实现面最小、稳定性最高、迁移成本最低。
   - 退出条件：需求进入复杂表单、多步骤输入、富交互。
2. `Inline Keyboard + callback_query`
   - 进入条件：分支决策、确认/取消、分页、筛选、小型菜单。
   - 裁决理由：比纯文本命令更可控，误操作更少。
   - 退出条件：状态机迅速膨胀，或需要大块结构化输入。
3. `Reply Keyboard`
   - 进入条件：低认知成本的固定选项输入。
   - 禁止进入：复杂后台操作、敏感操作确认、长生命周期状态菜单。
4. `Deep Link`
   - 进入条件：把外部入口、邀请、场景参数带入 Telegram 会话。
   - 联动要求：只与 `Bot command` 或 `Mini App` 联动，不单独承载完整业务流程。
5. `Mini App / WebApp`
   - 进入条件：表单、多字段编辑、复杂筛选、富展示、半应用化流程。
   - 裁决理由：交互能力最强，可承载真正的 user interface。
   - 强制要求：同时治理前端、后端会话和 Telegram 容器环境；不得被当成普通 H5。
6. `LoginUrl`
   - 进入条件：将 Telegram 身份与外部站点或后端会话关联。
   - 禁止进入：替代完整业务 UI。

## 选择规则
- 如果需求只是“触发动作 + 查看结果”，落 `Bot command` 或 `Inline Keyboard`。
- 如果需求涉及多字段输入、复杂回显、滚动列表、富状态面板，落 `Mini App`。
- 如果需求要从外部渠道带参数进入 Telegram，会话入口落 `Deep Link`。
- 如果需求要把 Telegram 身份对接外部站点登录，落 `LoginUrl`。
- 不要默认把复杂 UI 硬塞进消息流；Telegram Bot 消息流不是通用表单引擎。

## 局部规则
- 默认基于 Telegram Bot API 能力做用户接口；未经立项，不走用户账号自动化或 MTProto 路径。
- `callback_query` 交互必须按“快速确认 + 后续状态更新”思路设计，不把全部耗时工作卡在按钮响应上。
- Mini App 只负责交互层与临时视图状态；业务真值仍由后端掌控。
- 任何 Telegram UI 方案都要考虑移动端输入、消息滚动和历史消息干扰。

## 例外与门禁
- 若任务目标本质上是“复杂前端产品 UI”，必须联动 `Dev-VUE3-WebUI-Frontend`，本技能只负责 Telegram 容器边界。
- 若任务开始讨论项目目录、模块归属、部署对象，必须切换到 `Dev-ProjectStructure-Constitution`。
