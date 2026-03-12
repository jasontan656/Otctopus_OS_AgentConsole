# Cli_Toolbox 使用文档

适用技能：`Disabled-Octupos-FullStack`

## 工具清单
- `Cli_Toolbox.skill_runtime_contract`
- `Cli_Toolbox.skill_facade_contract`
- `Cli_Toolbox.stage_checklist`
- `Cli_Toolbox.stage_doc_contract`
- `Cli_Toolbox.stage_command_contract`
- `Cli_Toolbox.stage_graph_contract`
- `Cli_Toolbox.mother_doc_stage`
- `Cli_Toolbox.materialize_container_layout`
- `Cli_Toolbox.sync_mother_doc_navigation`
- `Cli_Toolbox.mother_doc_agents_contract`
- `Cli_Toolbox.mother_doc_agents_directive`
- `Cli_Toolbox.mother_doc_agents_scan`
- `Cli_Toolbox.mother_doc_agents_collect`
- `Cli_Toolbox.mother_doc_agents_push`
- `Cli_Toolbox.sync_mother_doc_status`
- `Cli_Toolbox.implementation_stage`
- `Cli_Toolbox.evidence_stage`
- `Cli_Toolbox.append_implementation_log`
- `Cli_Toolbox.append_deployment_log`
- `OS_Graph_Cli.*`

## 核心命令

- `python3 scripts/Cli_Toolbox.py skill-runtime-contract --json`
- `python3 scripts/Cli_Toolbox.py skill-facade-contract --json`
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
- `python3 scripts/os_graph_cli.py status`
- `python3 scripts/os_graph_cli.py sync-doc-bindings`
- `python3 scripts/os_graph_cli.py sync-evidence`
- `python3 scripts/os_graph_cli.py <analyze|list|query|context|impact|detect-changes|resource|map|wiki|cypher> [args...]`

## 结构结果

- `skill-runtime-contract` 会返回 skill 级运行合同，并显式声明 `CLI_JSON` 是运行态优先来源。
- `skill-facade-contract` 会返回 skill 级路由图，包括顶层常驻文档、阶段顺序、阶段 summary command 与专用子分支入口。
- `sync-mother-doc-navigation` 会返回：
  - `created_readmes`
  - `created_scope_docs`
  - `updated_agents`
  - `removed_legacy_indexes`
- `mother-doc-agents-scan` 会返回根 `AGENTS.md`、非法额外 `AGENTS.md` 和旧治理资产的扫描结果。
- `mother-doc-agents-collect` 会刷新：
  - `assets/managed_targets/Octopus_OS/AGENTS_human.md`
  - `assets/managed_targets/Octopus_OS/AGENTS_machine.json`
- `mother-doc-agents-push` 会返回组合结果：
  - `scan`
  - `collect`
- `updated_agents` 只对应 `Octopus_OS/Mother_Doc/**` 内的导航文件，不会写入实际工作目录容器。
- `sync-mother-doc-status` 会返回受影响文档的状态块更新结果。
- `append-implementation-log` 与 `append-deployment-log` 只允许在 `evidence` 或 `implementation -> evidence` 联动中调用。
- 上述日志命令会返回日志目标文件与本次写入摘要。
- 上述日志命令中的 `summary` 必须直接复用同轮 Git 提交 message。
- `os_graph_cli.py` 是 evidence graph 命令域专用子 CLI；统一 skill 入口共享，但 graph 命令域独立。
