---
name: "Meta-refactor-behavior-preserving"
description: "面向任意工件的行为保持型重构/迁移协议。用于当用户希望在 prompts、rules、workflows、docs 或 code 上做重构、迁移、整理、升级时，保持对消费者可观察效果不退化，不新增语义、不丢失语义，并且至少获得一个显式质量增益。"
---

# Meta-refactor-behavior-preserving

## 1. 目标
- 提供统一入口，处理“重构/迁移但必须保持行为”的任务。
- 将“行为”定义为特定消费者可观察到的外部效果，而不是文本表面相似。
- 要求在保持可观察效果等价的前提下，至少获得一个显式质量增益。

## 2. 可用工具
- 抽象层：
  - 本技能当前不提供 CLI。
  - 门面页只提供入口、边界与导航；详细协议后置到 `references/`。
- 业务需求层：
  - `runnable_artifacts`：
    - 读取 `references/modes/runnable_artifacts_mode.md`
    - 用于代码、脚本、工具、runner 等可执行工件的行为保持型重构。
  - `prompt_workflows`：
    - 读取 `references/modes/prompt_workflow_mode.md`
    - 用于 prompts、rules、workflow、constitution 等自然语言驱动工件的行为保持型重构。

## 3. 工作流约束
- 抽象层：
  - 先判定当前对象属于哪个模式，再进入对应后置协议。
  - 开始重构前，必须先写出 OEC（Observable-Effect Contract，可观察效果合同）。
  - 若无法写清 OEC，就说明还没有进入可重构状态。
- 业务需求层：
  - `runnable_artifacts`：
    - 只在目标工件主要靠机器执行来体现行为时进入此模式。
  - `prompt_workflows`：
    - 只在目标工件主要靠自然语言改变模型决策轨迹时进入此模式。
  - 混合场景：
    - 先跑 `prompt_workflows`，再跑 `runnable_artifacts`。

## 4. 规则约束
- 抽象层：
  - 本技能不是 family 技能，不是 router family index，也不再使用 subskill/family 描述。
  - 门面页禁止承载细节性协议正文；详细规则必须后置。
  - 任意重构都必须满足：不新增未经批准的语义、不丢失原有语义、原触发条件仍然成立。
- 业务需求层：
  - `runnable_artifacts`：
    - 必须使用其独立模式文档，不得依赖 `prompt_workflows` 文档补语义。
  - `prompt_workflows`：
    - 必须使用其独立模式文档，不得依赖 `runnable_artifacts` 文档补语义。

## 5. 方法论约束
- 抽象层：
  - 先定义消费者，再定义可观察效果，再定义允许变化项。
  - “前后一致”指向可观察效果等价，不指向文本逐字相同。
  - 质量增益必须显式命名，不能把“删掉可观察输出”伪装成优化。
- 业务需求层：
  - `runnable_artifacts`：
    - 以可执行 oracle、baseline 和 witness set 证明等价。
  - `prompt_workflows`：
    - 以触发矩阵、轨迹 oracle 与写回语义证明等价。

## 6. 内联导航索引
- 抽象层：
  - [可执行工件模式] -> [references/modes/runnable_artifacts_mode.md]
  - [提示/规则工作流模式] -> [references/modes/prompt_workflow_mode.md]
- 业务需求层：
  - `runnable_artifacts` -> [references/modes/runnable_artifacts_mode.md]
  - `prompt_workflows` -> [references/modes/prompt_workflow_mode.md]

## 7. 架构契约
```text
Meta-refactor-behavior-preserving/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── modes/
        ├── runnable_artifacts_mode.md
        └── prompt_workflow_mode.md
```
