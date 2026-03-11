---
doc_id: "tooling.development.entry"
doc_type: "tooling_development"
topic: "Development guidance for the staged frontend CLI and graph rebuild surface"
anchors:
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture overview expands the CLI and showroom split."
  - target: "../stages/40_STAGE_SHOWROOM_RUNTIME.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "Tooling development is tightly coupled with showroom runtime delivery."
---

# Cli_Toolbox Development

## 当前职责
- 输出 staged runtime contracts。
- 输出 stage-specific doc/command/graph contracts。
- 负责 self graph rebuild，供展厅消费。

## 开发原则
- CLI 合同改动时，必须同步更新：
  - `references/runtime/`
  - `references/stages/`
  - `references/tooling/`
  - `ui-dev/docs/` 中受影响的运行面文档
- 若 stage 语义变了，优先整体改 stage manifest，而不是局部补丁。
