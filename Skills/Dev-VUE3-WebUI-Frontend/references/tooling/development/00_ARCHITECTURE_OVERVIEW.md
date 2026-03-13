---
doc_id: "tooling.architecture.overview"
doc_type: "tooling_architecture"
topic: "Architecture overview for staged frontend contracts, doc graph core, and product-runtime handoff"
anchors:
  - target: "modules/mod_stage_contract_runtime.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The stage-contract module explains the CLI contract layer."
---

# Architecture Overview

## 两层结构
- `resident + stage docs`
  - 负责前端标准、stage 顺序与人类审计入口。
- `root TS CLI + doc graph core`
  - 负责输出 machine-readable stage contracts、self graph 与产品运行时 handoff 规则。

## 关键边界
- stage contracts 在 root 输出，不写入产品代码仓。
- 技能自身只负责合同与 graph，不负责产品 UI 实现目录。
- 新的前端规范若要落地成运行界面，必须同时更新 stage docs 与产品侧 mother doc。
