---
doc_id: "ui.dev.docs.index"
doc_type: "ui_dev_index"
topic: "Index of frontend development contracts for Dev-VUE3-WebUI-Frontend"
node_role: "index_doc"
domain_type: "frontend_contract_index"
anchors:
  - target: "../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "The showroom consumes this frontend contract index as its official reading path."
  - target: "positioning/00_POSITIONING_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Positioning and file-boundary contracts form the first branch of the frontend contract tree."
  - target: "showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Showroom runtime contracts form the second branch of the frontend contract tree."
  - target: "rules/00_RULES_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Layout and responsive rules form the rule branch of the frontend contract tree."
---

# Frontend Development Contracts

## 分支读序
- `positioning/00_POSITIONING_INDEX.md`
  - 负责合同定位、目录边界、文件组织。
- `showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md`
  - 负责 viewer stack、运行链、服务工作流。
- `rules/00_RULES_INDEX.md`
  - 负责布局调整与响应式约束。

## 最小读取路径
1. 先读 `positioning/00_POSITIONING_INDEX.md`，确认这个目录在整个 skill 里的职责。
2. 再读 `showroom_runtime/00_SHOWROOM_RUNTIME_INDEX.md`，确认展厅运行面和复用面。
3. 最后读 `rules/00_RULES_INDEX.md`，收敛到具体布局规则。
