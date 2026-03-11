---
doc_id: "ui.viewer.service_workflow"
doc_type: "tooling_usage"
topic: "Dev, build, and systemd workflow for the Meta-VUE3-WebUI-frontend showroom"
anchors:
  - target: "VIEWER_STACK_AND_REUSE.md"
    relation: "operates"
    direction: "upstream"
    reason: "This workflow doc operates the stack defined there."
  - target: "../UI_DEV_ENTRY.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This workflow belongs to the ui-dev root."
---

# Viewer Service Workflow

## Dev 模式
- `npm install`
- `npm run dev`
- 修改 skill 内 markdown、json、yaml 后，watcher 会推送新 payload。
- viewer 运行时只读 skill 内容，不负责写回 root 规则文档。

## Prod 模式
- `npm run build`
- `npm run start`

## systemd
- `npm run service:install`
- 默认安装 user-level service：`meta-vue3-webui-frontend-viewer.service`
