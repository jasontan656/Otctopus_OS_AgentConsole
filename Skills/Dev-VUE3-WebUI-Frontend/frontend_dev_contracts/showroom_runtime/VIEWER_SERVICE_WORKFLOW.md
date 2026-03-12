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
---

# Viewer Service Workflow

## 当前状态
- `ui-dev/` 当前处于 docs-first redevelopment 状态。
- 旧 viewer runtime、前端依赖、build 产物和 service 安装链已经清空，不应继续被当成可运行入口。
- 在新的 SPA menu + canvas 实现落地前，本分支只定义未来恢复 runtime 时必须满足的工作流边界。

## 未来恢复条件
- 先完成 `ui-dev/docs/` 中的 showroom purpose、menu navigation、canvas workspace、panel catalog 文档。
- 再完成对应的前端合同收敛，尤其是 container hierarchy、layout authority、interaction protocol 与 English-only 语言规则。
- 最后才允许重新引入 dev/build/service 运行链。

## 恢复后约束
- 恢复 runtime 时仍只能消费归一化后的 `PreviewPayload`。
- 恢复 runtime 时必须先把 dev/build/service 命令重新写回 `ui-dev/UI_DEV_ENTRY.md`、`SKILL.md` 与 stage command contract。
