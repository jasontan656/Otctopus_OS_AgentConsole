---
doc_id: "runtime.contract.audit"
doc_type: "runtime_contract"
topic: "Audit version of the staged runtime contract for Dev-VUE3-WebUI-Frontend"
anchors:
  - target: "../stages/00_STAGE_INDEX.md"
    relation: "details"
    direction: "downstream"
    reason: "The stage index expands the runtime contract into explicit stage order and resident docs."
  - target: "../stages/01_RESIDENT_FRONTEND_NORTH_STAR.md"
    relation: "governed_by"
    direction: "downstream"
    reason: "The resident north-star doc carries the long-lived boundary referenced by this runtime contract."
---

# Runtime Contract

## 合同目标
- 约束 `Dev-VUE3-WebUI-Frontend` 只能以 staged skill 方式运行。
- 把前端规范、展厅设计、graph 展示与 showroom redevelopment docs 拆成可切换的 stage。
- 保证阶段切换后只保留 resident docs，而不把局部实现上下文跨阶段带走。

## 常驻文档
- `SKILL.md`
- `references/runtime/SKILL_RUNTIME_CONTRACT.md`
- `references/stages/00_STAGE_INDEX.md`
- `references/stages/01_RESIDENT_FRONTEND_NORTH_STAR.md`

## 阶段集合
- `foundation_north_star`
- `responsive_surface_system`
- `motion_component_architecture`
- `showroom_runtime_delivery`

## 统一入口
- `npm run cli -- runtime-contract --json`
- `npm run cli -- stage-checklist --stage <stage> --json`
- `npm run cli -- stage-doc-contract --stage <stage> --json`
- `npm run cli -- stage-command-contract --stage <stage> --json`
- `npm run cli -- stage-graph-contract --stage <stage> --json`

## 运行门禁
- 未读取当前阶段四类合同前，不得开始该阶段动作。
- 阶段切换后，必须丢弃上一阶段 checklist、stage docs 与临时 focus。
- UI 展厅修改必须同时考虑：
  - 文档 graph 可读性
  - SPA menu + canvas 工作区目标
  - UI 自身开发文档边界
  - 下一轮代码重建的契约完备度
