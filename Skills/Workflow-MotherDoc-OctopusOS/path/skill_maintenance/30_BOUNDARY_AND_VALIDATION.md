---
doc_id: workflow_motherdoc_octopusos.path.skill_maintenance.boundary_validation
doc_type: topic_atom
topic: Workflow-MotherDoc-OctopusOS self maintenance boundary and validation
---

# 稳定边界与收口校验

## 与现有 mother_doc 主入口的稳定边界
- `stage_flow` 继续负责真实 `mother_doc` 阶段执行，`skill_maintenance` 不替代它，也不绕过它。
- 当任务是在写回 `Octopus_OS/Development_Docs/mother_doc` 的真实内容时，应以 `stage_flow` 为主；`skill_maintenance` 只负责同步改善本技能自身如何服务这类任务。
- `skill_maintenance` 可以调整本技能内部文档结构，但不能把业务执行规则偷偷移出 `stage_flow` 的可发现面。

## 与下游阶段技能的稳定边界
- `Workflow-ConstructionPlan-OctopusOS` 仍只消费已确认、已 lint 的 `mother_doc` 设计切片；当前入口不得重写它的 pack 语义。
- `Workflow-Implementation-OctopusOS` 仍只消费 active pack；当前入口不得把 implementation 细节塞回本技能的常驻合同。
- `Workflow-Acceptance-OctopusOS` 仍负责真实 witness 与交付收口；当前入口不得把 acceptance 判定提前吸收到 `mother_doc` 或技能治理层。

## 当前入口的最小验证清单
- `SKILL.md` 中的功能入口列表与实际 `path/` 目录保持一致。
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry stage_flow --json` 仍可正常编译。
- `python3 ./scripts/Cli_Toolbox.py read-contract-context --entry skill_maintenance --json` 可正常编译。
- 本轮若调整了职责边界，`SKILL.md`、对应 path 文档与必要测试已同步更新。
- 本轮若发生正文迁移，旧位置没有残留并行真源。
