# 2-Octupos-FullStack Runtime Contract

> Audit copy for `references/runtime/SKILL_RUNTIME_CONTRACT.json`.

- `skill_name`: `2-Octupos-FullStack`
- `role_definition`: 未来项目 admin panel 内置的运营AI“章鱼”，负责持续维护 `Mother_Doc`、开发代码并回填 evidence。
- `workspace_root`: `/home/jasontan656/AI_Projects/Octopus_OS`
- `mother_doc_container_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/`
- `document_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs/`
- `graph_asset_root`: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/`
- `always_load_rules`:
  - `rules/FULLSTACK_SKILL_HARD_RULES.md`
  - `references/runtime/SKILL_RUNTIME_CONTRACT.md`
  - `references/skill_native/00_SKILL_NATIVE_INDEX.md`
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
- `AGENTS.md` 只允许存在于 `Octopus_OS/Mother_Doc/**`，不得进入实际工作目录容器。
- `Mother_Doc` 每一层目录都必须具备 `README.md`、`AGENTS.md`、`<folder_name>.md`。
- 每个容器文档目录都必须固定具备 `overview/`、`features/`、`shared/`、`common/`。
- `AGENTS.md` 之外的 `Mother_Doc` markdown 必须具备 `Document Status + Block Registry`，供机械探测变动。
- `mother_doc` 阶段必须先用 `Meta-prompt-write` 强化用户意图，再读取 `mother_doc` 子分支入口判定当前任务链。
- `mother_doc` 阶段固定先判定 `direct_writeback`、`question_backfill` 或 `AGENTS manager`；不得混写。
- `AGENTS manager` 只管理 `Octopus_OS/Mother_Doc/docs/**/AGENTS.md`，并固定采用 `scan / collect / push` 三阶段。
- `direct_writeback` 只写已明确内容；`question_backfill` 只关闭未收口问题。
- `mother_doc` 更新文档后，必须把受影响文档/区块标记为 `pending_implementation`。
- `mother_doc` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕。
- `implementation` 阶段必须像独立开发者一样推进，并主动修复 doc-code drift。
- `implementation` 对齐完成后，必须把受影响文档/区块改回 `aligned`，并把对齐范围交给 `evidence` 统一留痕。
- `implementation` 阶段禁止写开发日志、部署日志与 Git / GitHub 留痕。
- `evidence` 阶段必须以 `OS_graph` 统一文档图、代码图与 evidence 绑定。
- `OS_graph` 固定区分 `narrative_layer`、`contract_layer`、`implementation_layer`、`evidence_layer`。
- `evidence` 阶段独占 implementation batch、deployment checkpoint 与 Git / GitHub 留痕。
- deployment-level witness 出现后，必须追加 deployment checkpoint 日志。
- 开发/部署日志只写摘要；摘要必须等于同轮 Git 提交 message，具体修改由 Git / GitHub 提供明细。
- 所有回填都采用覆盖写入，只维护当前状态；项目内部不保留文档版本，但日志保留时间线。
