---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.steps.research_baseline.entry
doc_type: action_entry_doc
topic: Research baseline stage for governing a target skill
reading_chain:
- key: architecture_convergence
  target: ../architecture_convergence/00_ARCHITECTURE_CONVERGENCE_ENTRY.md
  hop: next
  reason: 先建立现状与证据，再进入目标态收敛。
---

# research_baseline

## 阶段目标
- 调查目标技能当前真实状态、现有用途、当前结构、当前 tooling、当前缺陷与现有约束。

## 必须显式应用
- `Functional-Analysis-Runtask`：作为主研究闭环，组织证据采样与问题拆解。
- `SkillsManager-Creation-Template`：判断当前技能更接近什么 profile，以及目标态应收敛成什么 profile。
- `Dev-ProjectStructure-Constitution`：判断目标技能在项目内的定位、边界和不应越权承载的对象。

## 阶段产物
- 当前真实结构说明
- 当前问题与成因清单
- 候选目标 profile 与骨架判断
- 需要保持的行为与不应丢失的用途
- 回填 `stage_runtime_checklist`，并把 `research_baseline` 产物作为 `architecture_convergence` 的唯一前置输入
