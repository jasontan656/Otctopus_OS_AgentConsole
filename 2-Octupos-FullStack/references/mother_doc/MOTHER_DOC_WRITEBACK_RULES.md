# Mother_Doc Writeback Rules

适用技能：`2-Octupos-FullStack`

## Writeback Model

- `mother_doc` 回填采用覆盖写入。
- 项目内部不规划文档版本。
- 任何受影响目录都必须同步刷新：
  - `README.md`
  - `AGENTS.md`
  - `<folder_name>.md`
- 上述刷新只发生在 `Octopus_OS/Mother_Doc/**` 内，不写入实际工作目录容器。
- 任何受影响的非 `AGENTS.md` 文档都必须同步刷新 `Document Status + Block Registry`。
- 默认回填值固定为：
  - `doc_requires_development: true`
  - `doc_sync_status: pending_implementation`
  - `requires_development: true`
  - `sync_status: pending_implementation`

## Structural Rule

- 目录结构变化后，父层索引与当前层实体说明都必须同步更新。
- `Mother_Doc/docs/Mother_Doc/common/code_abstractions/` 下的系统级主链路文档必须保持可递归发现，不得散落到无关容器目录：
  - `architecture/doc_code_authority.md`
  - `architecture/semantic_coverage_unit.md`
  - `architecture/mother_doc_container_architecture.md`
  - `architecture/os_graph_layer_model.md`
  - `contracts/cross_container_contract_baseline.md`
  - `contracts/evidence_minimum_witness.md`
