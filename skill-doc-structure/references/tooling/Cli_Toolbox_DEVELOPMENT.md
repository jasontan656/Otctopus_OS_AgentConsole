---
doc_id: "tooling.development.entry"
doc_type: "tooling_development"
topic: "Development guidance for the document-structure CLI and graph core"
anchors:
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture overview expands the CLI and core-library split."
  - target: "development/modules/mod_docstructure_core.md"
    relation: "indexes"
    direction: "downstream"
    reason: "The core module doc explains the graph-building engine."
---

# Cli_Toolbox Development

## 当前职责
- 输出 runtime contract。
- 输出 markdown graph workspace。
- 输出 self graph rebuild。

## 开发原则
- 若 CLI 命令或 graph core 变更，必须同步更新 runtime contract、tooling docs 与测试。
- 本技能不再维护任何 UI 相关 runtime 文档。
