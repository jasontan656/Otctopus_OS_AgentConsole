---
name: Workflow-Implementation-OctopusOS
description: Octopus_OS 的 implementation 阶段技能；负责严格消费 active pack 并把实现与证据落盘。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: workflow_implementation_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-Implementation-OctopusOS skill
---

# Workflow-Implementation-OctopusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责 `implementation` 阶段。
- 它只消费当前 active pack，不重新发明新的任务切片。
- 实现、测试与 pack 级证据必须在这一阶段同步落盘。

### 2. 技能约束
- 只读取 active pack 与其声明的 `source_mother_doc_refs`。
- 不把 construction_plan 的切包语义带回 implementation 阶段。
- 当前阶段只通过本技能自己的 CLI 落地实现与证据。

### 3. 顶层常驻合同
- 当前阶段的实现必须解释为何满足 design intent，而不只是“代码看起来能跑”。
- 只有在本地实现与验证完成后，才允许推动 mother_doc state sync。

## 2. 功能入口
- [stage_flow]：`path/stage_flow/00_STAGE_FLOW_ENTRY.md`
  - 作用：进入 `implementation` 阶段的最小执行链。

## 3. 目录结构图
```text
Workflow-Implementation-OctopusOS/
├── SKILL.md
├── agents/
└── path/
    └── stage_flow/
```
