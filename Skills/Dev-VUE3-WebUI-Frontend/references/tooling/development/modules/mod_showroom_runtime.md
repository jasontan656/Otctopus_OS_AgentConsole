---
doc_id: "tooling.module.showroom_runtime"
doc_type: "module_doc"
topic: "Showroom runtime module for the Vue3 viewer, live payload server, and systemd path"
anchors:
  - target: "../00_ARCHITECTURE_OVERVIEW.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This module is part of the tooling architecture overview."
  - target: "../../../../ui-dev/UI_DEV_ENTRY.md"
    relation: "explained_by"
    direction: "downstream"
    reason: "The ui-dev entry expands how the showroom runtime is organized."
---

# Showroom Runtime Module

## 负责内容
- `ui-dev/UI_DEV_ENTRY.md`
- `ui-dev/docs/*`
- `frontend_dev_contracts/showroom_runtime/VIEWER_SERVICE_WORKFLOW.md`
- `frontend_dev_contracts/containers/*`
- `frontend_dev_contracts/layers/*`
- `frontend_dev_contracts/design_system/*`
- `frontend_dev_contracts/component_system/*`
- `frontend_dev_contracts/code_architecture/*`

## 设计意图
- 让 `ui-dev/` 先作为 showroom redevelopment docs root，避免旧 runnable UI 持续误导读者。
- 让 graph、menu、canvas、panel catalog 的目标形态先在文档里收敛，再进入下一轮代码重建。
