---
doc_id: "tooling.architecture.overview"
doc_type: "tooling_architecture"
topic: "Architecture overview of the TS CLI core and the embedded UI tool split"
anchors:
  - target: "../../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "Architecture exists to implement the runtime contract."
  - target: "modules/mod_viewer_runtime.md"
    relation: "decomposes_into"
    direction: "downstream"
    reason: "The viewer runtime module explains the frontend/server split."
---

# 架构总览

## 组件
- `scripts/Cli_Toolbox.ts`
  - TS CLI 入口。
- `src/lib/docstructure.ts`
  - 文档图谱、lint 与 graph 构建核心。
- `tests/test_cli_toolbox.spec.ts`
  - 根技能文档治理回归测试。
- `ui-dev/server/viewer-server.ts`
  - watcher server、API、websocket 与 Vite middleware。
- `ui-dev/lib/viewer-payload.ts`
  - UI payload 组装层。
- `ui-dev/client/*`
  - Vue3 + Vue Flow 门面页面。
- `ui-dev/docs/*`
  - UI 开发文档与布局调整规范。

## 设计主张
- 不再保留 Python 双轨。
- 根技能只维护文档治理核心；UI 只作为内置工具消费该核心。
- viewer 读取真实 markdown，而不是复制一份静态结构。
- UI 相关资产集中在 `ui-dev/`，便于后续单独调界面与维护前端文档。
