# Evidence Index

适用阶段：`evidence`

## Purpose

- `evidence` 是三阶段中的交付闭环层。
- 进入本阶段后，不要直接从总规则推理细节；先按子域入口继续读取。

## Branch Entry

- `graph`
  - [graph 子域入口](./graph/00_GRAPH_INDEX.md)
  - 负责 `OS_graph` runtime、查询、写回、变更检测与前端消费契约。
- `logs`
  - [implementation 日志规则](./IMPLEMENTATION_LOG_RULES.md)
  - [deployment 日志规则](./DEPLOYMENT_LOG_RULES.md)
- `bindings`
  - [doc-code 绑定规则](./DOC_CODE_BINDING_RULES.md)

## Entry Rule

- graph、logs、bindings 都属于 `evidence`，但不要混写。
- graph 子域是 evidence 的结构核心；logs 与 bindings 都要回收到 graph runtime 中。
