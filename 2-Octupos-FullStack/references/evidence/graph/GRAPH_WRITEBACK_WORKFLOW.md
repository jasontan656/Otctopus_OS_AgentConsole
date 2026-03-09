# Graph Writeback Workflow

适用阶段：`evidence > graph`

## Workflow

1. 承接 `mother_doc + implementation` 当前状态。
2. 先同步文档节点与层视图。
3. 再同步 evidence 节点与 lifecycle 索引。
4. 再运行 analyze/query/context/impact/detect-changes 等 graph 能力。
5. 将 witness、logs、bindings 与 graph 统一回写到 runtime root。
6. 已闭环范围再回写文档/区块状态为 `developed`。

## Prohibition

- 不得在 `mother_doc` 直接写 graph runtime。
- 不得把 graph writeback 与 Git/GitHub 留痕切开；二者都属于 `evidence` 闭环。
