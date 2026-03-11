---
doc_id: "tooling.architecture.overview"
doc_type: "tooling_architecture"
topic: "Architecture overview for staged frontend contracts, doc graph core, and runnable showroom"
anchors:
  - target: "modules/mod_stage_contract_runtime.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The stage-contract module explains the CLI contract layer."
  - target: "modules/mod_showroom_runtime.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The showroom runtime module explains the runnable ui-dev layer."
---

# Architecture Overview

## 三层结构
- `resident + stage docs`
  - 负责前端标准、stage 顺序与人类审计入口。
- `root TS CLI + doc graph core`
  - 负责输出 machine-readable stage contracts 与 self graph。
- `ui-dev runnable showroom`
  - 负责把当前技能文档真实渲染为人类可视界面。

## 关键边界
- stage contracts 在 root 输出，不放到 `ui-dev` 内随意漂移。
- `ui-dev` 消费 root graph core，但不再跨技能 import。
- 新的前端规范若要落地成运行界面，必须同时更新 stage docs 与 `ui-dev`。
