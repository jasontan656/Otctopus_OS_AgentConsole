---
doc_id: workflow_centralflow2_octppusos.path.development_loop.steps.mother_doc.workflow_index
doc_type: workflow_index_doc
topic: Mother doc workflow index
reading_chain:
- key: scope_and_runtime
  target: steps/scope_and_runtime/00_SCOPE_AND_RUNTIME_ENTRY.md
  hop: branch
  reason: 先锁定 docs_root 与当前轮文档容器。
- key: protocol_tree
  target: steps/protocol_tree/00_PROTOCOL_TREE_ENTRY.md
  hop: branch
  reason: 再固化协议驱动文档树。
- key: state_and_sync
  target: steps/state_and_sync/00_STATE_AND_SYNC_ENTRY.md
  hop: branch
  reason: 然后处理状态迁移与 client mirror 同步。
- key: lint_and_exit
  target: steps/lint_and_exit/00_LINT_AND_EXIT_ENTRY.md
  hop: branch
  reason: 最后完成 lint 与退出门。
---

# mother_doc 子 workflow 索引

## 当前阶段的复合步骤
1. [scope_and_runtime]：`steps/scope_and_runtime/00_SCOPE_AND_RUNTIME_ENTRY.md`
2. [protocol_tree]：`steps/protocol_tree/00_PROTOCOL_TREE_ENTRY.md`
3. [state_and_sync]：`steps/state_and_sync/00_STATE_AND_SYNC_ENTRY.md`
4. [lint_and_exit]：`steps/lint_and_exit/00_LINT_AND_EXIT_ENTRY.md`

## 下一跳列表
- [scope_and_runtime]：`steps/scope_and_runtime/00_SCOPE_AND_RUNTIME_ENTRY.md`
- [protocol_tree]：`steps/protocol_tree/00_PROTOCOL_TREE_ENTRY.md`
- [state_and_sync]：`steps/state_and_sync/00_STATE_AND_SYNC_ENTRY.md`
- [lint_and_exit]：`steps/lint_and_exit/00_LINT_AND_EXIT_ENTRY.md`
