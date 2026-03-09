# Evidence Stage

适用阶段：`evidence`

## Scope

- 从 `implementation` 当前状态中提取真实 witness。
- 以 `OS_graph` 统一文档 graph、代码 graph 与 evidence 绑定。
- 当存在可部署/已部署 witness 时追加 deployment checkpoint。

## Required Workflow

1. 显式承接 `mother_doc + implementation` 当前状态产物。
2. 以 `OS_graph` 的层级关系组织模块、helper、父级目录与 witness。
3. 把真实 evidence 回填到对应的文档节点与代码节点。
4. 如已形成真实部署/上线 witness，则追加 deployment checkpoint。
5. 覆盖写回当前状态，不保留项目内部版本分支。

## Produces

- execution evidence
- acceptance witnesses
- deployment checkpoints
- OS_graph contract-level writeback
