---
doc_id: "tooling.usage.cli"
doc_type: "tooling_usage"
topic: "CLI usage for staged frontend contracts and graph rebuild commands"
anchors:
  - target: "../runtime/SKILL_RUNTIME_CONTRACT.md"
    relation: "implements"
    direction: "upstream"
    reason: "The CLI is the machine-readable execution surface of the runtime contract."
  - target: "../stages/00_STAGE_INDEX.md"
    relation: "operates"
    direction: "upstream"
    reason: "Stage commands operate the stage sequence defined in the stage index."
---

# Cli_Toolbox Usage

## 命令集合
- `npm run cli -- runtime-contract --json`
- `npm run cli -- stage-checklist --stage <stage> --json`
- `npm run cli -- stage-doc-contract --stage <stage> --json`
- `npm run cli -- stage-command-contract --stage <stage> --json`
- `npm run cli -- stage-graph-contract --stage <stage> --json`
- `npm run cli -- build-anchor-graph --json`
- `npm run cli -- rebuild-self-graph --json`

## 使用原则
- staged skill 的当前阶段行为只能从 CLI JSON 获取。
- graph rebuild 用于让技能自身合同图保持最新。
- 若任务是产品 UI 运行层，CLI 只负责合同与 graph，不替代产品仓的 dev/build/service 命令。
