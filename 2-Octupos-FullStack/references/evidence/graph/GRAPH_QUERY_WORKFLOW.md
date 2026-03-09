# Graph Query Workflow

适用阶段：`evidence > graph`

## Query Modes

- `query`
- `context`
- `impact`
- `resource`
- `cypher`

## Query Rule

- CLI 查询优先命中 `runtime/registry` 与 `runtime/indexes`。
- 需要代码层深查时，再桥接底层 graph engine。
- 返回结果要能回指 authored docs、code slices 和 evidence nodes。
