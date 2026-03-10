---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "CLI usage for document-structure graph building and self-graph rebuild"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI is the machine-readable execution surface of the runtime contract."
  - target: "development/20_CATEGORY_INDEX.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The category index expands the tooling development reading path."
---

# Cli_Toolbox Usage

## 命令集合
- `npm run cli -- runtime-contract --json`
- `npm run cli -- build-anchor-graph --json`
- `npm run cli -- rebuild-self-graph --json`

## 使用原则
- graph 相关结论优先来自 CLI JSON，不直接从 markdown 规则推断。
- `rebuild-self-graph` 负责把当前 skill 的 graph 回写到 `assets/runtime/self_anchor_graph.json`。
