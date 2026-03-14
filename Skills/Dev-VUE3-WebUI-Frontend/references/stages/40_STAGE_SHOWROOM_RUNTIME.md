---
doc_id: "stages.product_runtime_handoff"
doc_type: "stage_doc"
topic: "Product runtime handoff stage for the Vue3 web UI frontend skill"
anchors:
  - target: "../../frontend_dev_contracts/layers/30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "details"
    direction: "downstream"
    reason: "The locator protocol defines the visible node identifiers that a product runtime must surface."
  - target: "../../frontend_dev_contracts/containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "details"
    direction: "downstream"
    reason: "The payload normalization contract defines the runtime bridge input boundary for a product runtime."
  - target: "../../frontend_dev_contracts/rules/UI_PACKAGE_SHAPE_LINT_WORKFLOW.md"
    relation: "details"
    direction: "downstream"
    reason: "The handoff stage also enforces component package shape and export discipline."
---

# Stage Product Runtime Handoff

## 本阶段负责
- 定义技能如何把具体产品运行时需求 handoff 到产品仓的 mother doc。
- 保持本技能只承载通用前端合同、运行时边界和 truthfulness，不回存产品级 menu/canvas/panel 需求。
- 要求人类先通过产品母文档确认工作台要展示什么，再进入下一轮代码重建。
- 保留 runtime bridge、workspace 容器、panel 容器与 locator 协议的目标叙事，但不假装当前技能内已经落地产品 UI。
- 定义文档 graph、代码 graph、AI 入口与多治理域自动发现的共通合同，不替代产品级 requirement source。

## 交付要求
- `frontend_dev_contracts/` 与阶段合同能够独立描述通用前端规范。
- 具体产品运行时需求落到产品仓的 `Workflow-CentralFlow1-OctopusOS mother_doc`。
- 当前 skill 内不再保留会误导读者的产品级 UI 代码、依赖或需求目录。
