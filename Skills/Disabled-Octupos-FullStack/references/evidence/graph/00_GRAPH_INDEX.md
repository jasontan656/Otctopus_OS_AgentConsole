# OS Graph Index

适用阶段：`evidence > graph`

## Purpose

- 这是 `OS_graph` 子域的单一入口。
- 从这里继续进入 runtime、命令、节点模型、存储布局、前端消费与迁移映射。

## Load Order

1. [runtime contract](./GRAPH_RUNTIME_CONTRACT.md)
2. [command contract](./GRAPH_COMMAND_CONTRACT.md)
3. [node and edge model](./GRAPH_NODE_EDGE_MODEL.md)
4. [storage layout](./GRAPH_STORAGE_LAYOUT.md)
5. [frontend consumption contract](./GRAPH_FRONTEND_CONSUMPTION_CONTRACT.md)
6. [writeback workflow](./GRAPH_WRITEBACK_WORKFLOW.md)
7. [change detection workflow](./GRAPH_CHANGE_DETECTION_WORKFLOW.md)
8. [query workflow](./GRAPH_QUERY_WORKFLOW.md)
9. [resource workflow](./GRAPH_RESOURCE_WORKFLOW.md)
10. [migration map](./GRAPH_MIGRATION_MAP.md)

## Rule

- graph 子域内每份文档只定义一个子问题。
- 如果同一问题既涉及 runtime 又涉及前端消费，优先分别写入对应合同文件，再通过入口索引串起来。
