---
doc_id: "ui.dev.container.payload_normalization"
doc_type: "tooling_architecture"
topic: "Payload normalization boundary for the showroom runtime and SPA containers"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_STATE_AND_DATA_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This contract belongs to the state and data branch."
  - target: "../../../references/stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The runtime handoff stage provides the runtime-source boundary that feeds the normalized payload."
  - target: "../interaction/10_CONTAINER_EVENT_AND_ROUTE_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Normalized payload is the input boundary for container interaction."
---

# Container Payload Normalization

## 归一化边界
- 当前技能不存放 runtime 代码，但未来产品实现仍必须保留清晰的归一化边界。
- 未来 runtime source 负责提供 raw runtime channel。
- 未来 payload adapter 负责把 graph workspace 归一化成 `PreviewPayload`。
- 未来 scene-level runtime bridge 负责消费 `PreviewPayload`，不在容器内部重新拼装 raw channel 数据。

## 容器消费规则
- 所有视觉容器只消费已经归一化的 `PreviewPayload` 或其派生只读数据。
- runtime 桥接负责 websocket reconnect、初始拉取、退化状态切换。
- 工作区级容器只处理 selection、search、layout 编排，不直接知道服务端 watcher 细节。
