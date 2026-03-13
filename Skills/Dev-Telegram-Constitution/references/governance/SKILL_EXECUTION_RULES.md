---
doc_id: dev_telegram_constitution.governance.execution_rules
doc_type: topic_atom
topic: Execution rules for the Telegram interface constitution skill
anchors:
- target: SKILL_DOCSTRUCTURE_POLICY.md
  relation: pairs_with
  direction: lateral
  reason: Execution rules and doc-structure policy should stay aligned.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing should send readers here for deep execution rules.
---

# Skill Execution Rules

## 本地目的
- 约束本技能如何回答 Telegram interface 相关问题。
- 避免把 Telegram 渠道讨论误写成前端、后端或项目结构全栈大杂烩。

## 当前边界
- 本技能只治理 Telegram 渠道能力、交互面、依赖栈与交付边界。
- 本技能不负责具体 handler 代码、数据库 schema、前端组件实现与项目目录落点。

## 局部规则
- 先判断需求是 `Bot 消息流`、`Inline/Reply Keyboard`、`Deep Link`、`LoginUrl` 还是 `Mini App`，再按对应合同裁决。
- 技术栈裁决默认基于 `Telegram Bot API` 主路径；没有单独立项时，禁止无证据扩张到用户账号自动化路径。
- 依赖文档必须显式区分 `已裁决`、`待用户裁决`、`禁止默认采用` 三种状态；不得只列框架名。
- 若某项依赖仍处于待用户裁决状态，AI 在执行过程中不得把候选方案写成既定方案。
- 讨论 Mini App 时，必须同时说明 Telegram 容器边界、服务端验证和与主前端规范的衔接。
- 若任务开始进入具体语言实现，必须切到对应 domain skill：
  - Python -> `Dev-PythonCode-Constitution`
  - 前端 UI -> `Dev-VUE3-WebUI-Frontend`
  - 项目结构 -> `Dev-OctopusOS-Constitution-ProjectStructure`

## 例外与门禁
- 若问题本质上是“写代码”而不是“定 Telegram 规范”，本技能只能先给边界，再路由到实现技能。
- 若问题涉及版本、依赖流行度或 Telegram 官方能力是否最新，必须以当时官方文档或主项目文档为准。
- 若用户要求自己裁决依赖选型，AI 必须先给候选方案、差异、进入条件与退出条件，再等待用户定版。
