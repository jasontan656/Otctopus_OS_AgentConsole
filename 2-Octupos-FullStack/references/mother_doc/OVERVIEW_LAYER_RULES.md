# Overview Layer Rules

适用阶段：`mother_doc`

## Role

- `overview/` 是当前容器的人类总览层。
- 人类进入容器后，优先从这里获得顶层理解。
- 这里不承载细节实现流程，只承载概括、地图与范围说明。

## Fixed Files

- `container_overview.md`
- `capability_map.md`
- `surface_index.md`

## Writing Rule

- 顶层先讲“这个容器是什么、负责什么、当前有什么”。
- 再指向 `features/` 与 `shared/`，不要在总览层展开全部细节。
- 文案优先服务人类理解，同时保持能被后续 `OS_graph` 当作 narrative_layer 消费。
