---
doc_id: "ui.viewer.service_workflow"
doc_type: "tooling_usage"
topic: "Dev, build, and systemd workflow for the Dev-VUE3-WebUI-Frontend showroom"
node_role: "topic_atom"
domain_type: "frontend_contract_atom"
anchors:
  - target: "00_SHOWROOM_RUNTIME_INDEX.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow belongs to the showroom runtime branch."
  - target: "../containers/state/20_CONTAINER_PAYLOAD_NORMALIZATION.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The service workflow feeds the normalized payload boundary consumed by UI containers."
  - target: "VIEWER_STACK_AND_REUSE.md"
    relation: "operates"
    direction: "upstream"
    reason: "This workflow doc operates the stack defined there."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "supports"
    direction: "upstream"
    reason: "This workflow drives the runnable showroom entry."
  - target: "../../ui-dev/docs/domains/20_DISCOVERY_AND_RENDERING_PROTOCOL.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The runtime restore workflow depends on a stable discovery and rendering protocol."
---

# Viewer Service Workflow

## 当前状态
- `ui-dev/` 当前处于 docs-first redevelopment 状态。
- 旧 viewer runtime、前端依赖、build 产物和 service 安装链已经清空，不应继续被当成可运行入口。
- 在新的 SPA menu + canvas 实现落地前，本分支只定义未来恢复 runtime 时必须满足的工作流边界。
- code graph 数据面仍由 `Meta-code-graph-base` 生成，但最终界面承载方已经固定为本技能定义的统一工作台。

## 未来恢复条件
- 先完成 `ui-dev/docs/` 中的 showroom purpose、domain model、discovery protocol、menu navigation、canvas workspace、panel catalog 文档。
- 再完成对应的前端合同收敛，尤其是 container hierarchy、layout authority、interaction protocol 与 English-only 语言规则。
- 再确认 `document_graph` 与 `code_graph` 两类治理域都能通过 projection adapter 被同一前端壳读取。
- 最后才允许重新引入 dev/build/service 运行链。

## 恢复后约束
- 恢复 runtime 时仍只能消费归一化后的 `PreviewPayload`。
- 恢复 runtime 时必须先把 dev/build/service 命令重新写回 `ui-dev/UI_DEV_ENTRY.md`、`SKILL.md` 与 stage command contract。
- 恢复 runtime 时不得把 GitNexus 原前端直接嵌回 skill；只能提炼其交互能力并回收到本技能 menu/canvas/panel 架构之下。
