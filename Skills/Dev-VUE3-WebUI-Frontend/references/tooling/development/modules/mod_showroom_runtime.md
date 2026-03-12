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
- `ui-dev/server/viewer-server.ts`
- `ui-dev/client/*`
- `ui-dev/scripts/install_user_service.sh`
- `ui-dev/client/src/contracts/ui-identity-registry.ts`
- `ui-dev/client/src/styles/*`
- `ui-dev/client/src/components/*/index.ts`
- `frontend_dev_contracts/showroom_runtime/VIEWER_SERVICE_WORKFLOW.md`
- `frontend_dev_contracts/containers/*`
- `frontend_dev_contracts/layers/*`
- `frontend_dev_contracts/design_system/*`
- `frontend_dev_contracts/component_system/*`
- `frontend_dev_contracts/code_architecture/*`

## 设计意图
- 让网站既是技能门面，又是前端规范展厅。
- 让 graph 读取真实文档，而不是静态演示数据。
