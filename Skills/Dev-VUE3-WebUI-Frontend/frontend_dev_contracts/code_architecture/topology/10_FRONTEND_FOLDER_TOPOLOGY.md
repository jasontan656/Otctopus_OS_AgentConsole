---
doc_id: "ui.dev.code_architecture.folder_topology"
doc_type: "ui_dev_guide"
topic: "Frontend folder topology for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_TOPOLOGY_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "Folder topology belongs to the topology branch."
  - target: "../../positioning/UI_FILE_ORGANIZATION.md"
    relation: "refines"
    direction: "cross"
    reason: "This document refines the coarse file-organization contract."
---

# Frontend Folder Topology

## `ui-dev/client/src` 推荐拓扑
```text
client/src/
├── containers/
├── components/
│   └── ComponentName/
├── composables/
├── contracts/
├── styles/
├── App.vue
├── main.ts
└── types.ts
```

## 各目录职责
- `containers/`
  - scene、workspace、panel、overlay 容器编排。
- `components/`
  - folder-first 的共享或局部可复用组件 package。
- `composables/`
  - runtime bridge、locator state、派生 view model。
- `contracts/`
  - registry、typed contract、lint 可消费元数据。
- `styles/`
  - 全局 token、semantic、base、layout 资产。

## 禁止事项
- 不新增 `misc/`, `helpers/`, `shared-junk/` 一类杂散目录。
- 不把组件局部样式继续堆回单一全局 CSS 大文件。
