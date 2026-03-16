---
name: Workflow-Acceptance-OctopusOS
description: Octopus_OS 的 acceptance 阶段技能；负责真实 bring-up、witness 与交付收口。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: workflow_acceptance_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-Acceptance-OctopusOS skill
---

# Workflow-Acceptance-OctopusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责 `acceptance` 阶段。
- 它负责 bring-up、真实 witness、acceptance artifacts 与交付收口。
- 本技能不回头重写 mother doc 主题，也不重新切 pack。

### 2. 技能约束
- 先完成本地可控范围内的配置、运行与健康检查，再谈 `needs_real_env`。
- acceptance 只在真实证据、`acceptance-lint` 与 `graph-postflight` 收口后结束。
- 当前阶段只通过本技能自己的 CLI 完成交付收口。

### 3. 顶层常驻合同
- 交付判断必须基于真实 witness，而不是推测性结论。
- 只有在 acceptance 收口完成后，相关 mother doc 状态才允许推进到 `ref`。

## 2. 功能入口
- [stage_flow]：`path/stage_flow/00_STAGE_FLOW_ENTRY.md`
  - 作用：进入 `acceptance` 阶段的最小执行链。

## 3. 目录结构图
```text
Workflow-Acceptance-OctopusOS/
├── SKILL.md
├── agents/
└── path/
    └── stage_flow/
```
