# Mother_Doc Entry Rules

适用技能：`2-Octupos-FullStack`

## 入口定位

- 本文档定义 `Mother_Doc` 撰写/维护入口的运行规则。
- 它只定义 AI 如何判断是否需要新增容器与文档目录，以及这些目录的最低抽象层形态。
- `Mother_Doc` 当前入口形态应以同名容器目录为主，不保留 `01-07` 这类编号治理目录作为主要结构。
- `Mother_Doc/README.md` 是镜像根说明；`Mother_Doc/Mother_Doc/00_INDEX.md` 是 `Mother_Doc` 容器自己的索引。

## 动态扩充原则

- 容器目录参考内容可以静态存在，但真实容器集合不是封闭白名单。
- AI 必须依据用户的当前项目描述，判断是否需要横向新增容器目录。
- 若需求引入可独立部署、可独立演进或可独立承载职责的模块，AI 必须判定为可新增容器。

## 同步新增要求

若决定新增容器，必须同步新增：

- `Octopus_OS/<Container_Name>/`
- `Octopus_OS/Mother_Doc/<Container_Name>/`

二者必须保持同名，以便：

- 人类一眼对号
- UI 一眼映射
- AI 不需要额外维护名字映射表

`Mother_Doc` 特例：

- 工作目录容器本身就是 `Octopus_OS/Mother_Doc/`
- 其自描述文档目录应为 `Octopus_OS/Mother_Doc/Mother_Doc/`

## 抽象层协议

- 每个容器文档目录必须先固定为：
  - `README.md`
  - `common/`
- `common/` 当前固定 5 个一级域：
  - `architecture/`
  - `stack/`
  - `naming/`
  - `contracts/`
  - `operations/`
- 每个最小知识点单独一个 `*.md`。
- 新增容器后，必须同步生成其容器族对应的 `common/` 抽象层骨架。

## 容器族模板

- `Mother_Doc`:
  - `common/architecture/{role,boundary,container_mapping,visualization_mapping,writeback_model}.md`
  - `common/stack/{storage_model,access_model,graph_model,indexing_model}.md`
  - `common/naming/{directory_naming,file_naming,node_naming,container_naming}.md`
  - `common/contracts/{read_api,writeback_api,evidence_contract,sync_contract}.md`
  - `common/operations/{maintenance_entry,query_commands,change_policy,recovery_entry}.md`
- `UI`:
  - `common/architecture/{screen_map,component_layers,state_boundary,interaction_boundary}.md`
  - `common/stack/{framework_stack,styling_stack,build_stack,runtime_stack}.md`
  - `common/naming/{route_naming,component_naming,state_naming,event_naming}.md`
  - `common/contracts/{backend_api_usage,event_contract,permission_contract,error_feedback_contract}.md`
  - `common/operations/{release_entry,debug_commands,environment_notes}.md`
- `Gateway`:
  - `common/architecture/{routing_boundary,upstream_map,auth_forwarding,traffic_boundary}.md`
  - `common/stack/{gateway_stack,deployment_mode,runtime_profile}.md`
  - `common/naming/{route_prefixes,upstream_aliases,header_naming}.md`
  - `common/contracts/{inbound_contract,upstream_contract,auth_contract,error_contract}.md`
  - `common/operations/{rate_limit_policy,debug_commands,rollback_entry}.md`
- `Service`:
  - `common/architecture/{bounded_context,component_map,dependency_boundary,async_boundary}.md`
  - `common/stack/{runtime_stack,storage_stack,transport_stack,async_stack}.md`
  - `common/naming/{entity_naming,api_naming,event_naming,job_naming}.md`
  - `common/contracts/{inbound_api,outbound_api,event_contract,error_contract,healthcheck_contract}.md`
  - `common/operations/{deploy_entry,healthcheck,query_commands,recovery_entry}.md`
- `Data_Infra`:
  - `common/architecture/{role,ownership_boundary,client_boundary,data_boundary}.md`
  - `common/stack/{engine_profile,deployment_mode,persistence_profile}.md`
  - `common/naming/{resource_naming,namespace_naming,key_or_schema_naming}.md`
  - `common/contracts/{access_policy,client_contract,backup_restore_contract,retention_contract}.md`
  - `common/operations/{query_commands,maintenance_commands,recovery_entry,monitoring_entry}.md`

## 判定示例

- 若用户说需要 `MongoDB`，且它被作为独立技术模块引入，则 AI 应判定可以新增 `Mongo_DB/`。
- 若用户说需要单独的通知能力，则 AI 应判定可以新增 `Notification_Service/`。
- 若用户只是要求在现有服务内增加一个局部函数，不应默认新增容器。

## 边界

- 是否新增容器由 AI 基于项目语义判断。
- CLI 工具只负责根据 AI 已判定的结果落目录，不替代语义判断。
