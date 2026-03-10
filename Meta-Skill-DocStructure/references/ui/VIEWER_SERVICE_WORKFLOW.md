---
doc_id: "ui.viewer.service_workflow"
doc_type: "tooling_usage"
topic: "Dev, build, and systemd workflow for the Meta-Skill-DocStructure viewer"
anchors:
  - target: "VIEWER_STACK_AND_REUSE.md"
    relation: "operates"
    direction: "upstream"
    reason: "This workflow doc operates the stack defined there."
  - target: "../tooling/Cli_Toolbox_USAGE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "CLI usage and viewer operations should be read together."
---

# Viewer Service Workflow

## Dev 模式
- `npm install`
- `npm run dev`
- 修改 skill 内 markdown、json、yaml 后，watcher 会推送新 payload。
- 删除文档或新增文档后，viewer 的节点列表与 graph 会同步增减。

## Prod 模式
- `npm run build`
- `npm run start`

## systemd
- `npm run service:install`
- 默认安装 user-level service：`meta-skill-docstructure-viewer.service`
