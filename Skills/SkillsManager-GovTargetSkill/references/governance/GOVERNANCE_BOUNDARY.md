---
doc_id: skillsmanager_govtargetskill.references.governance.governance_boundary
doc_type: topic_atom
topic: Governance boundary for SkillsManager-GovTargetSkill
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: This governance note defines the stable boundary of the lightweight workflow skill.
---

# Governance Boundary

## 稳定边界
- 本技能稳定承载的是“治理目标技能的闭环入口”，不是独立方法论全集。
- 稳定真源是：
  - `analysis_loop` 的阶段顺序
  - 对 `Functional-Analysis-Runtask` 的主依托关系
  - 对下游治理技能的显式约束关系

## 不应长回来的内容
- 不应在本技能内复制 `Functional-Analysis-Runtask` 的方法论正文。
- 不应在本技能内长出自有 CLI、runtime contract JSON、tooling 审计器或 Python lint 工具。
- 不应把目标技能的具体业务规则固化进本技能门面。

## 改造方法约束
- 若后续要扩展本技能，优先收紧职责表达，而不是叠加更多治理壳。
- 若目标技能治理需要更多细则，应下沉到被依托的下游治理技能，而不是回灌到本技能。
