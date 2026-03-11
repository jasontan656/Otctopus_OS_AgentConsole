---
doc_id: "ui.dev.layers.taxonomy"
doc_type: "ui_dev_guide"
topic: "Fixed layer catalog for the Dev-VUE3-WebUI-Frontend SPA and showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_LAYERS_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This taxonomy belongs to the layers branch."
  - target: "../containers/model/10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Layer design and container role design must stay aligned."
  - target: "20_LAYER_NODE_MAPPING.md"
    relation: "feeds"
    direction: "downstream"
    reason: "The node mapping doc instantiates this layer catalog."
---

# Layer Taxonomy

## 固定 layer catalog
- `SH`
  - Shell layer，负责顶层页面骨架与全局 page chrome。
- `SC`
  - Scene layer，负责 route scene 入口与场景级编排。
- `RT`
  - Runtime layer，负责 payload bridge、live status、runtime handshake。
- `WK`
  - Workspace layer，负责多 panel 工作区编排与共享选择态。
- `PN`
  - Panel layer，负责 feature panel 容器本身。
- `AT`
  - Atom layer，负责卡片、输入、列表项等轻量 UI 原子件。
- `GV`
  - Graph view layer，负责 graph canvas 与 graph 可视表达。
- `DC`
  - Document content layer，负责正文阅读、anchor 阅读、warning 表达。
- `DX`
  - Developer locator layer，负责 AI / human 协作时的定位标识、legend、toggle。
- `OV`
  - Overlay layer，负责未来 modal、drawer、palette 等瞬时界面；即使当前未使用，也纳入固定 catalog。

## 约束
- 新的 UI 节点应先落到既有 layer，再考虑新增节点；不允许把新增 feature 当成新增 layer 的理由。
- layer id 固定为两个大写字母，作为所有容器与组件命名的第一段。
