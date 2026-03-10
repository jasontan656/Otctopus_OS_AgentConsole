---
doc_id: "tooling.module.stage_contract_runtime"
doc_type: "module_doc"
topic: "Stage-contract runtime module for the staged frontend skill"
anchors:
  - target: "../00_ARCHITECTURE_OVERVIEW.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This module is part of the tooling architecture overview."
  - target: "../../../stages/00_STAGE_INDEX.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI module operationalizes the stage index through machine-readable contracts."
---

# Stage Contract Runtime Module

## 负责内容
- 输出 runtime contract。
- 输出四类 stage contracts。
- 输出 self graph rebuild 结果。

## 设计意图
- 让 staged skill 的运行规则永远先于 markdown 叙事被消费。
- 让前端标准、graph 展示与 show-room 运行都能被同一条 CLI 合同链约束。
