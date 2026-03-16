---
name: Workflow-ConstructionPlan-OctopusOS
description: Octopus_OS 的 construction_plan 阶段技能；负责把已确认的文档切片拆成正式 execution packs。
skill_mode: guide_with_tool
metadata:
  doc_structure:
    doc_id: workflow_constructionplan_octopusos.entry.facade
    doc_type: skill_facade
    topic: Entry facade for the Workflow-ConstructionPlan-OctopusOS skill
---

# Workflow-ConstructionPlan-OctopusOS

## 1. 模型立刻需要知道的事情
### 1. 总览
- 本技能只负责 `construction_plan` 阶段。
- 它消费已通过 `mother-doc-lint` 的设计切片，把当前轮修改拆成正式 `execution_atom_plan_validation_packs`。
- 本技能不重新定义产品架构，也不重写 mother doc 的主题裁决。

### 2. 技能约束
- 只处理 pack 拆分、state sync 与计划根目录治理。
- 工作目录统一由本技能自己的 `target-runtime-contract` 解析。
- `official_plan` 与 `preview_skeleton` 必须显式区分。

### 3. 顶层常驻合同
- 从 `modified` 的 mother_doc 原子文档切入，不反向篡改上游架构判断。
- 每个 pack 必须声明 `source_mother_doc_refs`。
- 进入 implementation 前必须由用户显式切换到 `Workflow-Implementation-OctopusOS`。

## 2. 功能入口
- [stage_flow]：`path/stage_flow/00_STAGE_FLOW_ENTRY.md`
  - 作用：进入 `construction_plan` 阶段的最小执行链。

## 3. 目录结构图
```text
Workflow-ConstructionPlan-OctopusOS/
├── SKILL.md
├── agents/
└── path/
    └── stage_flow/
```
