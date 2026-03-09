# Cli_Toolbox 使用文档

适用技能：`2-Octupos-FullStack`

## 工具清单
- `Cli_Toolbox.stage_checklist`
- `Cli_Toolbox.stage_doc_contract`
- `Cli_Toolbox.stage_command_contract`
- `Cli_Toolbox.stage_graph_contract`
- `Cli_Toolbox.mother_doc_stage`
- `Cli_Toolbox.materialize_container_layout`
- `Cli_Toolbox.sync_mother_doc_navigation`
- `Cli_Toolbox.implementation_stage`
- `Cli_Toolbox.evidence_stage`

## 核心命令

- `python3 scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-doc-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-command-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-graph-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json`

## 结构结果

- `sync-mother-doc-navigation` 会返回：
  - `created_readmes`
  - `created_scope_docs`
  - `updated_agents`
  - `removed_legacy_indexes`
