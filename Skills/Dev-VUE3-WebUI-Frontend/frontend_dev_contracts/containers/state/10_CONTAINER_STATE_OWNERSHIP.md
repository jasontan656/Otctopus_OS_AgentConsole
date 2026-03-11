---
doc_id: "ui.dev.container.state_ownership"
doc_type: "ui_dev_guide"
topic: "State ownership boundaries for showroom containers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_STATE_AND_DATA_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This contract belongs to the state branch."
  - target: "20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "State ownership depends on normalized payload boundaries."
  - target: "../model/10_CONTAINER_ROLE_TAXONOMY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Role semantics and state ownership must stay aligned."
---

# Container State Ownership

## 状态归属
- `ShowroomRuntimeBridge`
  - 拥有 `payload`、`liveState`、runtime 错误退化状态。
- `ShowroomWorkspaceContainer`
  - 拥有 `selectedPath`、`searchKeyword`，并基于 payload 派生 `docs`、`filteredDocs`、`selectedDoc`。
- `RuntimeStatusContainer`
  - 只读 `payload.summary`、`payload.status`、`liveState`，不拥有新的业务状态。
- `GraphPanelContainer`
  - 只读 `docs`、`edges`、`selectedPath`，只通过 `select(path)` 向父容器发出选择意图。
- `DocumentNavigatorContainer`
  - 只读工作区数据并向父容器发出 `updateSearch` 与 `selectDoc`。
- `DocumentReaderContainer`
  - 只读 `selectedDoc` 及其衍生 markdown/html，不拥有独立选中态。

## 禁止状态
- `GraphCanvas` 不得拥有全局文档选择或 payload 刷新状态。
- `DocumentReaderContainer` 不得自行维护另一个当前文档主状态。
- `RuntimeStatusContainer` 不得兼任 route、selection 或 panel 布局控制。
