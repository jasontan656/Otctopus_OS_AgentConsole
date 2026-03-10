---
doc_id: "tooling.development.entry"
doc_type: "tooling_development"
topic: "Development navigation for the TypeScript CLI and the embedded UI tool boundary"
anchors:
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture overview is the first development read."
  - target: "../../ui-dev/UI_DEV_ENTRY.md"
    relation: "pairs_with"
    direction: "cross"
    reason: "The UI dev root explains where viewer files and docs now live."
---

# Cli_Toolbox 开发文档

## 阅读顺序
1. `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
2. `ui-dev/UI_DEV_ENTRY.md`
3. `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
4. `references/tooling/development/20_CATEGORY_INDEX.md`

## 同步维护要求
- 任何 CLI 或文档治理核心改动都必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `assets/runtime/anchor_query_matrix.json`
- 任何 UI 子工具改动都必须同步更新：
  - `ui-dev/docs/*`
  - `ui-dev/assets/systemd/meta-skill-docstructure-viewer.service`
  - `ui-dev/tests/*`
