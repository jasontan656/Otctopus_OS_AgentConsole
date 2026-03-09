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
- `Cli_Toolbox.mother_doc_agents_contract`
- `Cli_Toolbox.mother_doc_agents_directive`
- `Cli_Toolbox.mother_doc_agents_registry`
- `Cli_Toolbox.mother_doc_agents_scan`
- `Cli_Toolbox.mother_doc_agents_collect`
- `Cli_Toolbox.mother_doc_agents_push`
- `Cli_Toolbox.sync_mother_doc_status`
- `Cli_Toolbox.implementation_stage`
- `Cli_Toolbox.evidence_stage`
- `Cli_Toolbox.append_implementation_log`
- `Cli_Toolbox.append_deployment_log`

## 核心命令

- `python3 scripts/Cli_Toolbox.py stage-checklist --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-doc-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-command-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py stage-graph-contract --stage <mother_doc|implementation|evidence> --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-navigation --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-contract --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-directive --stage <scan|collect|push> --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-scan --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-collect --json`
- `python3 scripts/Cli_Toolbox.py mother-doc-agents-push --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-status --stage <mother_doc|implementation|evidence> --path <relative-path> --lifecycle-state <modified|developed|null> --json`
- `python3 scripts/Cli_Toolbox.py sync-mother-doc-status-from-git --repo-root /home/jasontan656/AI_Projects/Octopus_OS --stage mother_doc --path <relative-path> --json`
- `python3 scripts/Cli_Toolbox.py append-implementation-log --summary "<git-commit-message>" --doc-path <doc-path> --code-path <code-path> --json`
- `python3 scripts/Cli_Toolbox.py append-deployment-log --summary "<git-commit-message>" --doc-path <doc-path> --code-path <code-path> --json`

## 结构结果

- `sync-mother-doc-navigation` 会返回：
  - `created_readmes`
  - `created_scope_docs`
  - `updated_agents`
  - `removed_legacy_indexes`
- `mother-doc-agents-scan` 会返回当前 `AGENTS.md` 覆盖面、缺失目录和遗留小写文件。
- `mother-doc-agents-collect` 会刷新：
  - `assets/mother_doc_agents/registry.json`
  - `assets/mother_doc_agents/index.md`
  - `assets/mother_doc_agents/collected_tree/`
- `mother-doc-agents-push` 会返回组合结果：
  - `navigation_sync`
  - `scan`
  - `collect`
- `updated_agents` 只对应 `Octopus_OS/Mother_Doc/**` 内的导航文件，不会写入实际工作目录容器。
- `sync-mother-doc-status` 会返回受影响文档的状态块更新结果。
- `append-implementation-log` 与 `append-deployment-log` 只允许在 `evidence` 或 `implementation -> evidence` 联动中调用。
- 上述日志命令会返回日志目标文件与本次写入摘要。
- 上述日志命令中的 `summary` 必须直接复用同轮 Git 提交 message。
