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
- `Cli_Toolbox.sync_mother_doc_status`
- `Cli_Toolbox.implementation_stage`
- `Cli_Toolbox.append_implementation_log`
- `Cli_Toolbox.evidence_stage`
- `Cli_Toolbox.append_deployment_log`

## 核心命令

- `python3 scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-doc-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-command-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-graph-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-status --stage <mother_doc|implementation|evidence> --path <relative-path> --sync-status <pending_implementation|aligned> [--requires-development|--no-requires-development] --json`
- `python3 scripts/Cli_Toolbox.py append-implementation-log --summary "<summary>" --doc-path <doc-path> --code-path <code-path> --json`
- `python3 scripts/Cli_Toolbox.py append-deployment-log --summary "<summary>" --doc-path <doc-path> --code-path <code-path> --json`

## 结构结果

- `sync-mother-doc-navigation` 会返回：
  - `created_readmes`
  - `created_scope_docs`
  - `updated_agents`
  - `removed_legacy_indexes`
- `updated_agents` 只对应 `Octopus_OS/Mother_Doc/**` 内的导航文件，不会写入实际工作目录容器。
- `sync-mother-doc-status` 会返回受影响文档的状态块更新结果。
- `append-implementation-log` 与 `append-deployment-log` 会返回日志目标文件与本次写入摘要。
