---
name: "temp-plan"
description: 用于在创建或规划开发相关技能前，快速注入用户当前长期开发意图、技能化优先策略与 OK 边界，避免每次重复补充背景。
---

# Temp-Plan

## 1. 定位
- 本文件只做门面入口，不承载规则正文。
- 本技能的唯一主轴是：把用户当前长期开发意图固化为可复用背景，让模型快速理解“现在在做什么、为什么这样做、做到什么程度算 OK”。
- 本技能是纯方法论背景注入技能，不提供本地 CLI，也不承载 repo 级运行态合同。

## 2. 必读顺序
1. 先读取 `references/current_intent.md`。
2. 再读取 `references/application_contract.md`。
3. 若当前任务是创建、改造或安装新的开发技能，转入 `$skill-creation-template` 作为具体模板治理入口。
4. 进入具体任务后，只保留“长期开发意图、技能化策略、OK 边界”这三个 focus；丢弃与当前任务无关的实现细节联想。

## 3. 分类入口
- 意图背景层：
  - `references/current_intent.md`
- 使用合同层：
  - `references/application_contract.md`
- 治理说明层：
  - `references/tooling/`
- 工具层：
  - 无本地 `Cli_Toolbox.py`；本技能不提供 CLI。
- 运行边界层：
  - workspace/root `AGENTS.md`
  - concrete repo local `AGENTS.md`
  - `$skill-creation-template`

## 4. 适用域
- 适用于：在创建、规划、评审开发相关技能前，快速让模型理解用户当前长期开发策略与背景。
- 适用于：需要知道为什么要先沉淀公共框架、规范、组件复用与示例资产，再进入具体开发。
- 不适用于：替代具体领域技能本身的实现规则、脚本能力、组件规范或 repo-specific 合同。
- 所有后续被创建的开发相关技能，仍应由 `$skill-creation-template` 负责具体结构治理。

## 5. 执行入口
- 统一入口：
  - 触发本技能后，按 `references/current_intent.md -> references/application_contract.md` 的顺序读取。
- 对齐入口：
  - 若任务是新技能建设，先用本技能缩小背景边界，再转入 `$skill-creation-template`。
  - 若任务是具体开发执行，先判断哪些公共定义应沉淀为技能，再决定是否进入具体 repo work。
- 合同入口：
  - 无 runtime contract；本技能的有效内容来自静态参考文档。
- 资产入口：
  - 无固定脚本或模板资产入口。

## 6. 读取原则
- 门面只做路由，正文下沉到 `references/`。
- 需要什么读什么，不要把所有引用文档一次性展开成新的门面正文。
- 本技能是静态方法论技能，markdown 参考文档就是主规则源；不要虚构不存在的 CLI 合同。
- 默认将“先定义框架与公共规范，再进入开发”视为优先策略，避免把公共定义散落到项目各处。
- 当用户要为某个开发主题建立长期复用能力时，优先判断是否应单独创建技能承载该主题。
- 所有新建开发技能都要遵循 `$skill-creation-template`，而不是临时自造结构。
- 若本技能的意图、边界或 OK 定义变化，同步更新门面、参考文档与 tooling 说明。

## 7. 结构索引
```text
temp-plan/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── current_intent.md
│   ├── application_contract.md
│   └── tooling/
└── assets/
```
