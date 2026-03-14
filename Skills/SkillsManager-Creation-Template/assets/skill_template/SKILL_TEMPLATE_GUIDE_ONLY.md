---
name: ${skill_name}
description: ${description}
skill_mode: guide_only
---

# ${skill_name}

## 1. 技能定位
- 本技能采用 `guide_only` 形态。
- 本文件就是技能本体，不再下沉到其他文档或专属 CLI。
- 规则、边界、示例与输出要求都必须直接写在当前 `SKILL.md`。

## 2. 适用域
- 适用于：[明确本方法论负责的唯一主轴]
- 不适用于：[明确排除域，避免与其他技能重叠]

## 3. 输入与输出
- 输入：[任务输入、上下文依赖、必要前置条件]
- 输出：[目标结果、建议格式、完成判据]

## 4. 执行规则
- 模型直接顺序读取本文件，不依赖额外 routing/doc tree/runtime contract。
- 若存在固定步骤，请在本节用稳定顺序写清楚。
- 若存在术语、禁区、优先级或裁决条件，也统一留在本节。

## 5. 维护约束
- `guide_only` skill 默认不受 `SkillsManager-Doc-Structure` 文档树 lint 约束。
- `guide_only` skill 默认不受 `SkillsManager-Tooling-CheckUp` 的 CLI/runtime-contract 形态审计。
- 当内容开始出现多个稳定分叉轴线、额外工具面或运行时合同需求时，应升级到 `guide_with_tool` 或 `executable_workflow_skill`。
