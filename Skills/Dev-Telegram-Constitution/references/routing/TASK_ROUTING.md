---
doc_id: dev_telegram_constitution.routing.task_routing
doc_type: routing_doc
topic: Task routing for the Telegram interface constitution skill
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The skill facade routes into this task routing doc.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Telegram task routing must always pass through the doc-structure policy.
---

# Task Routing

## 当前分叉轴线
- 本文件按“Telegram 问题类型”做单轴分流。
- 先判断当前问题属于哪一类，再读取一个主原子文档；不要一次性把所有原子文档全部展开。

## 分支一：能力面与交互入口
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`
- 再读 `../governance/SKILL_EXECUTION_RULES.md`
- 再进入 `../telegram/TELEGRAM_CAPABILITY_LANDSCAPE.md`
- 再进入 `../telegram/TELEGRAM_INTERFACE_SURFACES.md`
- 适用：Bot command、callback、deep link、reply keyboard、LoginUrl、Mini App 的主线裁决

## 分支二：技术栈与依赖选型
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`
- 再读 `../governance/SKILL_EXECUTION_RULES.md`
- 再进入 `../telegram/TELEGRAM_STACK_BASELINE.md`
- 适用：Python/TypeScript 框架、依赖组合、Bot API 路线的已裁决状态与待裁决候选集

## 分支三：交付、安全与消息流边界
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`
- 再读 `../governance/SKILL_EXECUTION_RULES.md`
- 再进入 `../telegram/TELEGRAM_DELIVERY_GUARDRAILS.md`
- 适用：webhook、getUpdates、callback、幂等、payload normalize、token 与日志边界的执行门禁

## 分支四：Mini App / WebApp 合同
- 先读 `../governance/SKILL_DOCSTRUCTURE_POLICY.md`
- 再读 `../governance/SKILL_EXECUTION_RULES.md`
- 再进入 `../telegram/TELEGRAM_MINI_APP_RULES.md`
- 适用：Mini App 容器边界、init data 验证、前后端协同、Bot 与 Mini App 的强制分工
