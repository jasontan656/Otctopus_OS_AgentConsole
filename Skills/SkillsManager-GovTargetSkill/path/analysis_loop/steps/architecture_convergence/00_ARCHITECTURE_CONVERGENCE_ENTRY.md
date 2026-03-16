---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.steps.architecture_convergence.entry
doc_type: action_entry_doc
topic: Architecture convergence stage for governing a target skill
reading_chain:
- key: plan
  target: ../plan/00_PLAN_ENTRY.md
  hop: next
  reason: 在目标态稳定后，再进入实施计划。
---

# architecture_convergence

## 阶段目标
- 把目标技能收敛到最终工程形态，明确什么保留、什么删除、什么重写、什么替换、什么下放。

## 必须显式应用
- `Functional-Analysis-Runtask`：负责把现状问题收敛成目标态架构结论。
- `Meta-keyword-first-edit`：要求优先删掉重写或整体替换，不在旧结构上叠补丁。
- `SkillsManager-Creation-Template`：确认目标态 profile、骨架与职责边界是否稳定。
- `Dev-ProjectStructure-Constitution`：确认目录、模块、上游/下游对象定位不漂移。

## 阶段产物
- 最终目标态描述
- 保留/删除/重写/替换/下放清单
- 重构方式裁决与无痕边界
- 回填 `stage_runtime_checklist`，并把架构收敛结果写成 `plan` 的唯一前置输入
