# Graph Command Contract


## Contract Header
- `contract_name`: `2_octupos_fullstack_references_evidence_graph_graph_command_contract`
- `contract_version`: `1.0.0`
- `validation_mode`: `strict`
- `required_fields`:
  - `contract_name`
  - `contract_version`
  - `validation_mode`
- `optional_fields`:
  - `notes`

适用阶段：`evidence > graph`

## Unified Entry

- `python3 scripts/os_graph_cli.py <command> [args...]`

## Native Commands

- `status`: 查看 runtime 与 vendored engine 就绪状态。
- `sync-doc-bindings`: 把 `Mother_Doc/docs` 编成文档节点、边与前端层视图。
- `sync-evidence`: 把 development logs 与 lifecycle 状态编成 evidence 侧节点与索引。

## Bridged Commands

- `analyze`
- `status`
- `list`
- `clean`
- `query`
- `context`
- `impact`
- `detect-changes`
- `rename`
- `augment`
- `resource`
- `map`
- `wiki`
- `cypher`

## Scope Rule

- 上述 graph 命令域只属于 `evidence`。
- 不得在 `mother_doc` 或 `implementation` 调用 graph 写回命令。
