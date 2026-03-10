# Graph Runtime Contract


## Contract Header
- `contract_name`: `2_octupos_fullstack_references_evidence_graph_graph_runtime_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

适用阶段：`evidence > graph`

## Roots

- graph asset root: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/`
- runtime root: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/graph/runtime/`
- document root: `/home/jasontan656/AI_Projects/Octopus_OS/Mother_Doc/docs/`

## Runtime Scopes

- `registry/`: node-level registries for documents and evidence.
- `indexes/`: edge indexes, lifecycle indexes, and query-facing binding data.
- `reports/`: sync and detect-changes reports.
- `maps/`: resource and graph-derived structural maps.
- `wiki/`: local graph-derived wiki bundles.
- `snapshots/`: future compare artifacts.
- `frontend_views/`: human-facing aggregated bundles derived from fragmented storage.

## Git Boundary

- `Mother_Doc/graph/` 是固定资产根，保留在仓库中。
- `Mother_Doc/graph/runtime/` 只保留目录骨架与 `README.md`。
- runtime 下的 generated json / kuzu / map / wiki / frontend bundles 默认是本地产物，必须由 `.gitignore` 排除，不作为长期跟踪资产提交。

## Bridge Rule

- 当前 CLI 与 runtime 已内生到章鱼OS evidence。
- 底层 engine 固定内置于 `2-Octupos-FullStack/assets/os_graph_engine/gitnexus_core`，由 evidence 阶段统一安装、构建与调用。
- 对模型而言，运行入口已经是章鱼OS evidence 子域 CLI，而不是外部 skill。
