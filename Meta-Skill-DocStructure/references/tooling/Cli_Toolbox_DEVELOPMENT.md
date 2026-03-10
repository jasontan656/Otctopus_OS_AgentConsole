---
doc_id: "tooling.development.entry"
doc_type: "tooling_development"
topic: "Development navigation for the TypeScript CLI and viewer runtime"
anchors:
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture overview is the first development read."
  - target: "../ui/VIEWER_STACK_AND_REUSE.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The viewer stack doc explains the frontend runtime."
---

# Cli_Toolbox 开发文档

## 阅读顺序
1. `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
2. `references/ui/VIEWER_STACK_AND_REUSE.md`
3. `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
4. `references/tooling/development/20_CATEGORY_INDEX.md`

## 同步维护要求
- 任何 CLI、server、viewer 改动都必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `references/ui/*`
  - `assets/runtime/anchor_query_matrix.json`
  - `assets/systemd/meta-skill-docstructure-viewer.service`
