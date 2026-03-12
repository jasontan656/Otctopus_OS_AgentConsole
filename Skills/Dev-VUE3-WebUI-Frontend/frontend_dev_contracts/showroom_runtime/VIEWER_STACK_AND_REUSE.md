---
doc_id: "ui.viewer.stack"
doc_type: "tooling_architecture"
topic: "Viewer stack, reusable UI direction, and showroom layout contract"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_SHOWROOM_RUNTIME_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This contract belongs to the showroom runtime branch."
  - target: "../containers/00_CONTAINERS_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The showroom stack is implemented through the SPA container tree."
  - target: "../layers/00_LAYERS_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The showroom stack must also follow the fixed layer catalog and locator protocol."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "This stack contract is consumed by the runnable showroom entry."
  - target: "../rules/UI_LAYOUT_ADJUSTMENT_RULES.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layout adjustment rules complement the stack contract."
---

# Viewer Stack Reuse Contract

## 当前定位
- showroom 当前先以开发文档形态存在，不再保留旧 runnable UI。
- 本文定义的是下一轮重建时必须遵守的目标 runtime 形态，而不是描述当前存量代码。

## 复用方向
- showroom 的目标形态必须是 `SPA shell + expandable menu + canvas workspace`。
- 菜单不是固定三栏中的一列，而是可展开、可收起、可继续扩展的导航入口。
- canvas workspace 不是静态排版区，而是用于承载已打开 panel 的活动组织面。
- panel 必须支持新增到 canvas、关闭、聚焦，以及后续扩展交互。
- graph、document library、document reader、runtime summary 都属于可装载到 canvas 的 panel 类型。
- 页面可见文案必须全部使用 English；代码、命名与注释也必须全部使用 English。
