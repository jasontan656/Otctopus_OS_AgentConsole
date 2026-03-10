# 2-Octupos-FullStack Runtime Contract


## Contract Header
- `contract_name`: `2_octupos_fullstack_references_runtime_skill_runtime_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `role_definition`: 未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- `workspace_root`: `/home/jasontan656/AI_Projects/Octopus_OS`
- `mother_doc_container_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`
- `document_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs/`
- `graph_asset_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/`
- `os_graph_runtime_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/runtime/`
- `always_load_rules`:
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - `references/skill_native/00_SKILL_NATIVE_INDEX.md`
  - `references/skill_native/10_PROJECT_BASELINE_INDEX.md`
  - `references/authored_domains/00_DOMAIN_INDEX.md`
  - `references/tooling/SKILL_TOOLING_WORKFLOW_CONTRACT.md`
  - `/home/jasontan656/AI_Projects/AGENTS.md`
- `stages`:
  - `mother_doc`
  - `implementation`
  - `evidence`

## Governance Rules
- 进入任一阶段前，固定先读 `stage-checklist`、`stage-doc-contract`、`stage-command-contract`、`stage-graph-contract`。
- 阶段切换时，只保留顶层常驻文档，再重读当前阶段合同。
- `AGENTS.md` 允许存在于 3 类路径：`Octopus_OS/AGENTS.md`、`Octopus_OS/<Container_Name>/AGENTS.md`、`Octopus_OS/Mother_Doc/docs/**/AGENTS.md`。
- `Mother_Doc` 每一层目录都必须具备 `README.md`、`AGENTS.md`、`<folder_name>.md`。
- 每个容器文档目录都必须固定具备 `overview/`、`features/`、`shared/`、`common/`。
- `AGENTS.md` 之外的 `Mother_Doc` markdown 必须具备 `Document Status + Block Registry`，供机械探测变动。
- `mother_doc` 阶段必须先用 `Meta-prompt-write` 强化用户意图，再读取 `mother_doc` 子分支入口判定当前任务链。
- `project baseline` 属于 always-load 层；进入任何具体容器或域前，固定先读。
- `mother_doc` 阶段固定先判定 `direct_writeback`、`question_backfill` 或 `AGENTS/README manager`；不得混写。
- `mother_doc` 的影响面判断固定采用“默认全相关 -> 排除高概率不相关项”。
- `AGENTS/README manager` 统一管理 `Octopus_OS` 根层、各容器根层与 `Mother_Doc/docs` 文档树的 `AGENTS.md + README.md`，并固定采用 `scan / collect / push` 三阶段。
- `direct_writeback` 只写已明确内容；`question_backfill` 只关闭未收口问题。
- `mother_doc` 更新文档后，必须运行本地 `git` 驱动的状态脚本；变更文档标记为 `modified`，空占位标记为 `null`。
- `mother_doc` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕。
- `implementation` 阶段必须像独立开发者一样推进，并主动修复 doc-code drift。
- `implementation` 只消费 `modified` 状态并完成代码对齐，不在本阶段回写 `developed`。
- `implementation` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕。
- `evidence` 阶段必须以 `OS_graph` 统一文档图、代码图与 evidence 绑定。
- `OS_graph` 固定区分 `narrative_layer`、`contract_layer`、`implementation_layer`、`evidence_layer`。
- `evidence` 固定先读 `references/evidence/00_EVIDENCE_INDEX.md`，再按 graph 子域入口继续读取。
- graph 命令域统一入口为 `python3 scripts/os_graph_cli.py <command> [args...]`。
- `evidence` 闭环完成后，必须把对应文档/区块状态回写为 `developed`。
- `evidence` 阶段独占 implementation batch、deployment checkpoint 与 Git / GitHub 留痕。
- deployment-level witness 出现后，必须追加 deployment checkpoint 日志。
- 开发/部署日志只写摘要；摘要必须等于同轮 Git 提交 message，具体修改由 Git / GitHub 提供明细。
- 所有回填都采用覆盖写入，只维护当前状态；项目内部不保留文档版本，但日志保留时间线。
