---
doc_id: workflow_motherdoc_octopusos.path.skill_maintenance.contract
doc_type: topic_atom
topic: Workflow-MotherDoc-OctopusOS self maintenance contract
reading_chain:
- key: layering
  target: 20_LAYERING_AND_SKELETON.md
  hop: next
  reason: 在稳定合同后继续读当前演进骨架与分层原则。
---

# 技能自维护合同

## 当前动作要完成什么
- 持续把 `Workflow-MotherDoc-OctopusOS` 维护成一个可演进、可迁移、可持续整理的技能，而不是一次性定死的文档壳。
- 在每一回合主动从用户输入里提炼对流程设计、文档分层、文件夹架构、锚点体系、撰写规范、文档职责边界和阶段衔接有价值的信息。
- 把这些信息反映到本技能自己的文档结构与维护机制上，并在需要时同步迁移既有内容。

## 当前动作必须满足什么
- `stage_flow` 仍是本技能的业务主入口；`skill_maintenance` 只是本技能自身的治理入口。
- 所有重构都必须保持以下可观察效果不退化：
  - `mother_doc` 仍然只负责把需求逐层写入既有文档体系。
  - 更深锚点主题仍然必须由用户显式指定。
  - `Workflow-ConstructionPlan-OctopusOS`、`Workflow-Implementation-OctopusOS` 与 `Workflow-Acceptance-OctopusOS` 仍然通过显式切换进入。
- 允许新增、拆分、合并、移动或重命名本技能内部文档与文件夹，但必须同步迁移正文、更新入口链、清理旧真源并补齐必要验证。
- 当任务已经越过本技能边界，触及 repo 级治理、根文件治理或其他阶段技能正文时，必须切回对应技能，不在当前入口里越界代办。

## 这一入口如何理解用户输入
- 流程类输入：既判断当前流程要怎样改，也判断本技能是否需要新的流程说明或分支入口。
- 文档类输入：既判断写到哪一层，也判断当前文档层级是否需要拆分、合并或迁移。
- 前端呈现、锚点规范、阶段衔接类输入：既判断它们在 `mother_doc` 的业务语义位置，也判断本技能是否需要新增稳定承载位来长期接住这类主题。

## 下一跳列表
- [layering]：`20_LAYERING_AND_SKELETON.md`
