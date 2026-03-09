# Graph Runtime Contract

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

## Bridge Rule

- 当前 CLI 与 runtime 已内生到章鱼OS evidence。
- 底层 engine 在本阶段通过 `Meta-code-graph-base/assets/gitnexus_core` 做 bridge source，直到后续 vendoring 独立完成。
- 对模型而言，运行入口已经是章鱼OS evidence 子域 CLI，而不是外部 skill。
