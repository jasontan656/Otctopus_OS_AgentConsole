---
doc_id: "ui.dev.layers.node_mapping"
doc_type: "ui_dev_guide"
topic: "Mapping between layers, containers, components, and their runtime files"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_LAYERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This mapping belongs to the layers branch."
  - target: "../containers/00_CONTAINERS_INDEX.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Container contracts define the container side of this mapping."
  - target: "30_LOCATOR_AND_IDENTIFIER_PROTOCOL.md"
    relation: "feeds"
    direction: "downstream"
    reason: "The locator protocol renders this mapping visible to humans."
---

# Layer Node Mapping

## 容器命名规则
- 容器 id 固定为 `layerId-containerName`。
- 当前容器映射：
  - `SH-AppShell`
  - `SC-ShowroomRouteScene`
  - `RT-ShowroomRuntimeBridge`
  - `RT-RuntimeStatus`
  - `WK-ShowroomWorkspace`
  - `PN-DocumentNavigator`
  - `PN-GraphPanel`
  - `PN-DocumentReader`
  - `DX-LocatorOverlay`

## 组件命名规则
- 组件 id 固定为 `layerId-containerName-componentName`。
- 当前组件映射至少覆盖：
  - `DX-LocatorOverlay-LocatorFrame`
  - `DX-LocatorOverlay-LocatorToolbar`
  - `DX-LocatorOverlay-LocatorLegend`
  - `AT-RuntimeStatus-StatCard`
  - `AT-DocumentNavigator-SearchBox`
  - `AT-DocumentNavigator-DocItem`
  - `GV-GraphPanel-GraphCanvas`
  - `DC-DocumentReader-DetailHero`
  - `DC-DocumentReader-AnchorChip`
  - `DC-DocumentReader-WarningList`
  - `DC-DocumentReader-MarkdownBody`

## 设计约束
- 组件必须同时绑定所属 layer 与所属 container，不允许只给组件名。
- registry 文件必须成为 layer、container、component 的单一 source of truth。
