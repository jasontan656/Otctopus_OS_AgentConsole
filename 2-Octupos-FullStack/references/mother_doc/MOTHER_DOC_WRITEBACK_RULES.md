# Mother_Doc Writeback Rules

适用技能：`2-Octupos-FullStack`

## Writeback Model

- `mother_doc` 回填采用覆盖写入。
- 项目内部不规划文档版本。
- 任何受影响目录都必须同步刷新：
  - `README.md`
  - `AGENTS.md`
  - `<folder_name>.md`
- 任何受影响容器都必须优先判断是否需要同步刷新：
  - `overview/`
  - `features/`
  - `shared/`
  - `common/`
- 上述刷新只发生在 `Octopus_OS/Mother_Doc/**` 内，不写入实际工作目录容器。
- 任何受影响的非 `AGENTS.md` 文档都必须同步刷新 `Document Status + Block Registry`。
- `mother_doc` 结束前必须运行本地 `git` 驱动的状态脚本：
  - 有差异 -> `modified`
  - 无差异但已是已开发状态 -> 保持 `developed`
  - 暂不适用或正文为空 -> `null`
- `mother_doc` 阶段不直接写 `developed`；`developed` 只能由 `evidence` 在闭环完成后回写。

## Structural Rule

- 目录结构变化后，父层索引与当前层实体说明都必须同步更新。
- `direct_writeback` 只写用户已明确描述的内容，未收口部分允许保留缺口。
- `question_backfill` 只负责收束缺口；回填后覆盖原文档，不保留并行版本。
- 问题缺口固定写入：
  - `features/open_questions.md`
  - `shared/open_questions.md`
- `Mother_Doc/docs/Mother_Doc/common/code_abstractions/` 下的系统级主链路文档必须保持可递归发现，不得散落到无关容器目录：
  - `architecture/doc_code_authority.md`
  - `architecture/semantic_coverage_unit.md`
  - `architecture/mother_doc_container_architecture.md`
  - `architecture/authored_doc_layer_model.md`
  - `architecture/question_backfill_model.md`
  - `architecture/os_graph_layer_model.md`
  - `contracts/cross_container_contract_baseline.md`
  - `contracts/doc_code_binding_contract.md`
  - `contracts/document_lifecycle_status_contract.md`
  - `contracts/evidence_minimum_witness.md`
