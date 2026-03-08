# 2-Octupos-FullStack Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `profile`: `staged_cli_first`
- `stage_axis`: `mother_doc -> construction_plan -> implementation -> acceptance`
- `SKILL.md` role: entry only
- Runtime guidance source:
  - 当前：`references/runtime/SKILL_RUNTIME_CONTRACT.json`
  - 后续：`Cli_Toolbox` commands
- Markdown role: human audit and reference

## Scope Categories
- `frontend`
- `backend`
- `database`
- `api_and_contracts`
- `deployment_and_runtime`
- `operations_and_maintenance`
- `app_and_multi_client`
- `integration_and_messaging`
- `testing_and_acceptance`
- `observability_and_security`
- `documentation_and_mother_doc_governance`
- `fullstack_graph_and_architecture_contracts`

## Governance Rules
- `SKILL.md` 必须保持轻量入口，不承载堆积式细节。
- 在阶段级 CLI 合同尚未完成前，以 `references/runtime/SKILL_RUNTIME_CONTRACT.json` 作为静态运行合同源；CLI 完成后切换为 CLI-first。
- `mother_doc` 是顶层需求源与长期维护容器。
- `fullstack graph` 不能替代 `mother_doc` 作为需求源。
- 公共内核只承载跨域稳定规则；域差异规则必须以下沉 overlay 承载。
- 阶段切换时只保留 resident docs，并显式丢弃上一阶段 focus。
- 技能内部规则不得覆盖 workspace/runtime 的外层硬合同。
- 若规则依赖真实项目状态，必须显式标记为 dynamic runtime contract。

## Tool Contracts
- `Cli_Toolbox.stage-checklist`: reserved interface
- `Cli_Toolbox.stage-doc-contract`: reserved interface
- `Cli_Toolbox.stage-command-contract`: reserved interface
- `Cli_Toolbox.stage-graph-contract`: reserved interface
