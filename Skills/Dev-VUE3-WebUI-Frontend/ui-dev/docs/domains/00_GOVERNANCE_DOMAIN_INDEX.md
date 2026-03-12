---
doc_id: "ui.dev.docs.domains.index"
doc_type: "index_doc"
topic: "Index of governance-domain docs for the unified frontend workbench"
anchors:
  - target: "../00_UI_DEV_DOCS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This domain branch belongs to the showroom docs tree."
  - target: "10_UNIFIED_GOVERNANCE_WORKBENCH_MODEL.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The domain model is the first branch-specific contract."
  - target: "20_DISCOVERY_AND_RENDERING_PROTOCOL.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The discovery protocol defines how governed sources become UI-readable."
---

# Governance Domain Index

## 本分支负责
- `10_UNIFIED_GOVERNANCE_WORKBENCH_MODEL.md`
  - 定义统一前端壳如何同时承载多个治理域而不压平语义。
- `20_DISCOVERY_AND_RENDERING_PROTOCOL.md`
  - 定义 UI 如何依据目录结构、manifest 与字段合同自动发现可展示内容。

## 读取顺序
1. `10_UNIFIED_GOVERNANCE_WORKBENCH_MODEL.md`
2. `20_DISCOVERY_AND_RENDERING_PROTOCOL.md`
