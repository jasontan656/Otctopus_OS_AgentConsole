# Evidence Stage

适用阶段：`evidence`

## Scope

- 从 `implementation` 当前状态中提取真实 witness。
- 以 `OS_graph` 统一文档 graph、代码 graph 与 evidence 绑定。
- 统一负责开发日志、部署日志与 Git / GitHub 留痕。

## Required Workflow

1. 显式承接 `mother_doc + implementation` 当前状态产物。
2. 以 `OS_graph` 的层级关系组织模块、helper、父级目录与 witness。
3. 先把 implementation 的对齐结果写成 implementation batch。
4. 把真实 evidence 回填到对应的文档节点与代码节点。
5. 如已形成真实部署/上线 witness，则追加 deployment checkpoint。
6. 在同轮留痕中统一写入 Git / GitHub 摘要追踪。
7. 覆盖写回当前状态，不保留项目内部版本分支。

## Produces

- execution evidence
- acceptance witnesses
- implementation batches
- deployment checkpoints
- OS_graph contract-level writeback
