---
doc_id: "tooling.module.viewer_runtime"
doc_type: "module_doc"
topic: "Viewer runtime module that binds watcher server, Vite, and Vue Flow"
anchors:
  - target: "../../../../ui-dev/docs/VIEWER_STACK_AND_REUSE.md"
    relation: "explained_by"
    direction: "upstream"
    reason: "The UI stack doc explains this module's stack choices."
  - target: "../../Cli_Toolbox_DEVELOPMENT.md"
    relation: "belongs_to"
    direction: "upstream"
    reason: "This module doc belongs to the tooling development tree."
---

# viewer_runtime 模块

## 职责
- 启动 express watcher server。
- 暴露 `/api/preview` 与 `/live`。
- dev 模式挂载 Vite middleware。
- prod 模式托管构建后的 client。
- 将 graph、正文、warning 实时推到页面。
- 所有运行文件都从 `ui-dev/` 子根目录启动与维护。
- UI payload 组装逻辑位于 `ui-dev/lib/viewer-payload.ts`。
- UI 相关测试位于 `ui-dev/tests/*`。
