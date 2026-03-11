# Graph Migration Map

适用阶段：`evidence > graph`

## Capability Mapping

- `Meta-code-graph-base analyze` -> `os_graph_cli analyze`
- `status` -> `os_graph_cli status`
- `list` -> `os_graph_cli list`
- `query` -> `os_graph_cli query`
- `context` -> `os_graph_cli context`
- `impact` -> `os_graph_cli impact`
- `detect-changes` -> `os_graph_cli detect-changes`
- `rename` -> `os_graph_cli rename`
- `augment` -> `os_graph_cli augment`
- `resource` -> `os_graph_cli resource`
- `map` -> `os_graph_cli map`
- `wiki` -> `os_graph_cli wiki`
- `cypher` -> `os_graph_cli cypher`
- new: `sync-doc-bindings`
- new: `sync-evidence`

## Migration Rule

- graph command surface 已迁入章鱼OS evidence。
- engine 已内迁到 `2-Octupos-FullStack/assets/os_graph_engine/gitnexus_core`；来源技能仅保留为历史来源，不再承担运行依赖。
