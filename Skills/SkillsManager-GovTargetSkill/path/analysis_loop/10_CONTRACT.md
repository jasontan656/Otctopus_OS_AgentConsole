---
doc_id: skillsmanager_govtargetskill.path.analysis_loop.contract
doc_type: action_contract_doc
topic: Analysis loop contract for governing a target skill
reading_chain:
- key: workflow_index
  target: 20_WORKFLOW_INDEX.md
  hop: next
  reason: 在确认边界与治理链之后，再进入固定阶段顺序。
---

# analysis_loop 合同

## 输入合同
- 当前闭环一次只治理一个目标技能。
- 输入必须至少包含以下两类信息：
  - 目标技能标识：技能名、技能根路径，或两者之一
  - 治理意图：当前问题、预期目标态、或需要保持的行为边界

## 角色分工
- `SkillsManager-GovTargetSkill`：
  - 负责路由、阶段边界、阶段产物与下游治理链显式挂接
- `Functional-Analysis-Runtask`：
  - 负责主执行闭环、调查证据组织、方案收敛、实施推进与验证闭合
- 其余治理技能：
  - 只作为约束源参与当前闭环，不升格为新的主闭环

## 必须显式应用的治理约束
- `SkillsManager-Creation-Template`
  - 用于决定目标技能应收敛成什么 `profile` 与骨架形态
- `Dev-ProjectStructure-Constitution`
  - 用于判断目标技能在 repo 内的结构定位、上下游边界与目录落点
- `SkillsManager-Tooling-CheckUp`
  - 用于审计目标技能的 CLI、runtime contract、artifact policy 与 remediation gate
- `Dev-PythonCode-Constitution`
  - 用于约束目标技能内 Python 代码、模块拆分、lint、pytest、runtime safety 与工具文档同步
- `Meta-keyword-first-edit`
  - 用于约束改造方式优先级为 `删掉重写 > keyword first 替换 > 新增`

## 预期产物
- `research_baseline`：当前技能真实现状、证据、问题清单与目标 profile 候选
- `architecture_convergence`：保留项、删除项、重写项、替换项、下放项与最终目标态
- `plan`：实施顺序、影响面、验证路径与风险边界
- `implementation`：实际落盘修改与同步更新的文档/代码/tooling 工件
- `validation`：结构、tooling、Python 与行为保持验证记录

## 行为保持边界
- 当前闭环默认以行为保持为前提，不凭空新增目标技能原本没有的业务语义。
- 可以清理过度个人化、补丁化或非标准承载方式，但不能删掉目标技能原有有效用途。
- 若出现方法论与工程稳定性冲突，优先沉淀稳定工程合同，把具体实现细节下放。

## 下一跳列表
- [workflow_index]：`20_WORKFLOW_INDEX.md`
