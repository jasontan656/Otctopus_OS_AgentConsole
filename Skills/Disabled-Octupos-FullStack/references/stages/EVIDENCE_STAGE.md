# Evidence Stage

适用阶段：`evidence`

## Scope

- 从 `implementation` 当前状态中提取真实 witness。
- 以 `OS_graph` 统一文档 graph、代码 graph 与 evidence 绑定。
- 统一负责开发日志、部署日志与 Git / GitHub 留痕。
- `OS_graph` 必须显式区分 `narrative_layer / contract_layer / implementation_layer / evidence_layer`。
- graph 细则固定从 `references/evidence/00_EVIDENCE_INDEX.md` 进入，再落到 `references/evidence/graph/00_GRAPH_INDEX.md`。

## Required Workflow

1. 显式承接 `mother_doc + implementation` 当前状态产物，并继续保留项目统一目标基线。
2. 以 `OS_graph` 的四层模型组织总览文档、共享合同、代码模块、helper、父级目录与 witness。
3. 把 graph 运行产物写回 `Octopus_OS/Mother_Doc/graph/`。
4. graph 命令域统一从 `./.venv_backend_skills/bin/python Skills/Disabled-Octupos-FullStack/scripts/os_graph_cli.py <command> [args...]` 进入，不得与其他阶段命令串用。
5. 先把 implementation 的对齐结果写成 implementation batch。
6. 把真实 evidence 回填到对应的文档节点与代码节点，并把已闭环范围的文档/区块状态回写为 `developed`。
7. 如已形成真实部署/上线 witness，则追加 deployment checkpoint。
8. 在同轮留痕中统一写入 Git / GitHub 摘要追踪。
9. 覆盖写回当前状态，不保留项目内部版本分支。

## Produces

- execution evidence
- acceptance witnesses
- implementation batches
- deployment checkpoints
- OS_graph contract-level writeback
- doc-code semantic bindings
