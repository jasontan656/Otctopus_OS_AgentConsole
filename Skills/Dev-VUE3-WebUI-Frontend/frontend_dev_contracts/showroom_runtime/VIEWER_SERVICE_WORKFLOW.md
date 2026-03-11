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

## Dev 模式
- `npm install`
- `npm run dev`
- 修改 skill 内 markdown、json、yaml 后，watcher 会推送新 payload。
- viewer 运行时只读 skill 内容，不负责写回 root 规则文档。
- browser 端容器只消费已经归一化的 `PreviewPayload`，不直接消费 watcher raw channel。

## Prod 模式
- `npm run build`
- `npm run start`

## systemd
- `npm run service:install`
- 默认安装 user-level service：`dev-vue3-webui-frontend-viewer.service`
