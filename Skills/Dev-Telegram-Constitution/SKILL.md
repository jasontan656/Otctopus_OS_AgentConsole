---
name: Dev-Telegram-Constitution
description: 将 Telegram 作为用户 interface 开发时的能力边界、交互裁决、技术栈选型状态与执行门禁写清楚。
metadata:
  doc_structure:
    doc_id: dev_telegram_constitution.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Dev-Telegram-Constitution skill
    anchors:
    - target: ./references/runtime_contracts/SKILL_RUNTIME_CONTRACT_human.md
      relation: routes_to
      direction: downstream
      reason: The facade routes runtime execution to the CLI-first contract.
---

# Dev-Telegram-Constitution

## Runtime Entry
- Primary runtime entry: `./.venv_backend_skills/bin/python Skills/Dev-Telegram-Constitution/scripts/Cli_Toolbox.py contract --json`
- CLI JSON is the primary runtime source; `SKILL.md` only remains as a facade and routing narrative.


## 1. 技能定位
- 本文件只做门面入口，不承载深规则正文。
- 本技能用于裁决“把 Telegram 作为用户 interface 开发”时的能力边界、交互入口、技术栈选型状态与交付门禁。
- 本技能聚焦 Telegram 渠道本身，不替代前端 UI 细节、项目结构、Python 代码实现或具体业务流程设计。
- 本技能当前是静态治理技能，没有专属 runtime contract，也没有本地 CLI；有效规则以下沉文档为准。

## 2. 必读顺序
1. 先读取 `references/routing/TASK_ROUTING.md`。
2. 再读取 `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`。
3. 再读取 `references/governance/SKILL_EXECUTION_RULES.md`。
4. 若任务在判定 Telegram 能做什么、当前需求应落哪种交互入口，再读取：
   - `references/telegram/TELEGRAM_CAPABILITY_LANDSCAPE.md`
   - `references/telegram/TELEGRAM_INTERFACE_SURFACES.md`
5. 若任务在判定框架、依赖、语言栈或当前已裁决/未裁决的选型状态，再读取：
   - `references/telegram/TELEGRAM_STACK_BASELINE.md`
6. 若任务在判定 webhook、回调、消息流、风控、安全边界，再读取：
   - `references/telegram/TELEGRAM_DELIVERY_GUARDRAILS.md`
7. 若任务在判定 Mini App / WebApp 的前后端边界与验证合同，再读取：
   - `references/telegram/TELEGRAM_MINI_APP_RULES.md`

## 3. 分类入口
- 路由层：
  - `references/routing/TASK_ROUTING.md`
- 治理层：
  - `references/governance/SKILL_DOCSTRUCTURE_POLICY.md`
  - `references/governance/SKILL_EXECUTION_RULES.md`
- Telegram 能力层：
  - `references/telegram/TELEGRAM_CAPABILITY_LANDSCAPE.md`
  - `references/telegram/TELEGRAM_INTERFACE_SURFACES.md`
  - `references/telegram/TELEGRAM_STACK_BASELINE.md`
  - `references/telegram/TELEGRAM_DELIVERY_GUARDRAILS.md`
  - `references/telegram/TELEGRAM_MINI_APP_RULES.md`
  - `references/telegram/TELEGRAM_BOT_INTERFACE_PRACTICES.md`
  - `references/telegram/TELEGRAM_INLINE_MODE_PRACTICES.md`
  - `references/telegram/TELEGRAM_ATTACHMENT_MENU_PRACTICES.md`
  - `references/telegram/TELEGRAM_PAYMENTS_AND_STARS.md`
  - `references/telegram/TELEGRAM_LOGIN_AND_IDENTITY.md`
  - `references/telegram/TELEGRAM_GAMES_AND_MEDIA.md`
  - `references/telegram/TELEGRAM_BUSINESS_INTEGRATION.md`
  - `references/telegram/TELEGRAM_FULL_API_CLIENTS.md`
- 工具层：
  - 当前无专属 CLI；`references/tooling/` 只保留“当前无工具”和未来扩展约束。

## 4. 适用域
- 适用于：Telegram Bot / Mini App / deep-link / callback / webhook 相关的产品入口设计、能力矩阵裁决、依赖选型状态、交互限制和交付门禁。
- 适用于：判断一个 Telegram 需求必须落在 Bot 消息流、Inline Keyboard、Reply Keyboard、Mini App、LoginUrl 或后台异步通知中的哪一种交互面。
- 适用于：管理 Python、TypeScript 或前端实现的当前已裁决栈与待裁决候选集。
- 不适用于：具体前端组件实现与视觉规范，这部分归 `Dev-VUE3-WebUI-Frontend`。
- 不适用于：项目级目录、部署对象、模块定位与系统结构，这部分归 `Dev-ProjectStructure-Constitution`。
- 不适用于：Python 代码落地、lint 与具体实现细则，这部分归 `Dev-PythonCode-Constitution`。

## 5. 执行入口
- 当前无专属 CLI。
- 当前入口即：`SKILL.md -> references/routing/TASK_ROUTING.md -> 对应 telegram 原子文档`。
- 若后续新增 Telegram contract checker、capability matrix generator 或 webhook checklist tool，必须同步更新 `references/tooling/` 全套文档。

## 6. 读取原则
- 门面只负责路由，不重新长回规则正文。
- `SkillsManager-Doc-Structure` 是创建与治理本技能时必须应用的显式规则。
- 若某条规则只属于单一 topic，应下沉到原子文档；不要继续堆在门面里。
- 先判断当前问题是在做“交互面裁决”“依赖选型裁决”“交付/安全边界裁决”还是 “Mini App 合同裁决”，再进入对应原子文档。
- Telegram 只是 interface/channel，不应把后端、数据库、前端三侧实现细节全部混回本技能。
- 若某项技术栈尚未被用户明确裁决，文档必须写成“待裁决状态”，AI 不得把候选方案伪装成既定方案。

## 7. 结构索引
```text
Dev-Telegram-Constitution/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
├── references/
│   ├── governance/
│   ├── routing/
│   ├── telegram/
│   └── tooling/
├── assets/
└── tests/
```
