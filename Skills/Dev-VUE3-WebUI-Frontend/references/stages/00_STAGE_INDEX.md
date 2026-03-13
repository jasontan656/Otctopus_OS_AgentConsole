---
doc_id: "stages.index"
doc_type: "stage_index"
topic: "Stage order and resident-doc routing for the Vue3 web UI frontend skill"
anchors:
  - target: "01_RESIDENT_FRONTEND_NORTH_STAR.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The resident north-star doc is always part of the stage path."
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The stage index instantiates the runtime contract into a concrete stage sequence."
---

# Stage Index

## 顶层常驻文档
- `SKILL.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/stages/00_STAGE_INDEX.md`
- `references/stages/01_RESIDENT_FRONTEND_NORTH_STAR.md`

## 统一入口
- `npm run cli -- stage-checklist --stage <stage> --json`
- `npm run cli -- stage-doc-contract --stage <stage> --json`
- `npm run cli -- stage-command-contract --stage <stage> --json`
- `npm run cli -- stage-graph-contract --stage <stage> --json`

## 阶段集合
| stage_id | objective | checklist | doc_contract | command_contract | graph_contract | exit_signal |
|---|---|---|---|---|---|---|
| `foundation_north_star` | 定义前端北极星与展厅角色 | `stage-checklist` | `stage-doc-contract` | `stage-command-contract` | `stage-graph-contract` | 北极星与 resident docs 稳定 |
| `responsive_surface_system` | 定义桌面与移动端表面规范 | `stage-checklist` | `stage-doc-contract` | `stage-command-contract` | `stage-graph-contract` | 响应式主叙事稳定 |
| `motion_component_architecture` | 定义动效、组件与代码组织 | `stage-checklist` | `stage-doc-contract` | `stage-command-contract` | `stage-graph-contract` | 组件边界和动效语义稳定 |
| `showroom_runtime_delivery` | 维持产品运行时 handoff 边界与合同诚实性 | `stage-checklist` | `stage-doc-contract` | `stage-command-contract` | `stage-graph-contract` | 技能不再存放产品需求且 handoff 语义稳定 |

## 切换规则
- 跨阶段只保留顶层常驻文档。
- 当前阶段完成后，显式丢弃上一阶段 checklist、stage docs 与临时 focus。
- 下一阶段开始前，重新读取该阶段四类合同。
