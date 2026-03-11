---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "CLI usage for document-structure graph building and self-graph rebuild"
anchors:
  - target: "../runtime/SKILL_DOCSTRUCTURE_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI is the machine-readable execution surface of the runtime contract."
  - target: "../methodology/SEMANTIC_ROUTING_TREE.md"
    relation: "routes_to"
    direction: "downstream"
    reason: "The semantic routing tree should be read before using CLI results to restructure docs."
---

# Cli_Toolbox Usage

## 命令集合
- `npm run cli -- runtime-contract --json`
- `npm run cli -- lint-split-points --target <skill_root> --json`
- `npm run cli -- register-split-decision --target <skill_root> --doc <doc_path> --rule <rule_id> --decision <accepted|split_required> --note <text> --json`
- `npm run cli -- build-anchor-graph --json`
- `npm run cli -- rebuild-self-graph --json`

## 使用原则
- 设计或改写文档树时，先读 `references/methodology/SEMANTIC_ROUTING_TREE.md`，再跑 CLI JSON。
- `lint-split-points` 命中后，默认视为阻断，不再只是 warning。
- 若用户明确决定当前文档暂不拆分，使用 `register-split-decision` 写入 registry。
- graph 相关结论优先来自 CLI JSON，不直接从 markdown 规则推断。
- `rebuild-self-graph` 负责把当前 skill 的 graph 回写到 `assets/runtime/self_anchor_graph.json`。
