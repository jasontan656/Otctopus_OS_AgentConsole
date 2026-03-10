---
doc_id: "tooling.development.entry"
doc_type: "tooling_development"
topic: "Cli_Toolbox development navigation for Meta-Skill-DocStructure"
anchors:
  - target: "development/00_ARCHITECTURE_OVERVIEW.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "Architecture overview is the first development read."
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "grounded_in"
    direction: "upstream"
    reason: "Development details must stay aligned with the runtime contract."
---

# Cli_Toolbox 开发文档

## 阅读顺序
1. `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md`
2. `references/tooling/development/00_ARCHITECTURE_OVERVIEW.md`
3. `references/tooling/development/20_CATEGORY_INDEX.md`
4. `references/tooling/development/modules/mod_runtime_contract.md`
5. `references/tooling/development/modules/mod_anchor_graph_lint.md`

## 同步维护要求
- 任何脚本改动都必须同步更新：
  - `references/tooling/Cli_Toolbox_USAGE.md`
  - `references/tooling/development/10_MODULE_CATALOG.yaml`
  - 相关模块文档
  - `references/runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.json`
  - `assets/runtime/anchor_query_matrix.json`
- 若改了本技能自己的 markdown 文档结构，必须运行：
  - `python3 scripts/Cli_Toolbox.py rebuild-self-graph --json`
