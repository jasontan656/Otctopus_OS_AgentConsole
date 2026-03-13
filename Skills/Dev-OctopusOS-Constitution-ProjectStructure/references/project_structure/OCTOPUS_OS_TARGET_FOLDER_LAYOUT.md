---
doc_id: dev_octopusos_constitution_projectstructure.project_structure.octopus_os_target_folder_layout
doc_type: topic_atom
topic: Concrete target folder layout for the Octopus_OS repository
anchors:
- target: FOLDER_CONTAINER_PLANNING_RULES.md
  relation: implements
  direction: upstream
  reason: This document materializes the folder and container planning rules.
- target: DOMAIN_OBJECT_POSITIONING_BOUNDARY.md
  relation: requires
  direction: upstream
  reason: The concrete layout follows the declared object classification.
---

# Octopus_OS Target Folder Layout

## 技能本体
- `/home/jasontan656/AI_Projects/Octopus_OS` 当前阶段的目标目录树固定如下。
- 旧目录内容仅视为历史残留，不再具有项目结构权威性。

## 目标树
```text
Octopus_OS/
├── AGENTS.md
├── README.md
├── Mother_Doc/
│   ├── Vision/
│   ├── Architecture/
│   ├── Roadmap/
│   └── Evidence/
├── System_Manifests/
│   ├── module_registry/
│   ├── tech_baseline/
│   └── deploy_matrix/
├── Octopus_Hub/
│   ├── Common/
│   ├── Core/
│   ├── Assets/
│   └── Development_Docs/
├── Foundation_Bundle/
│   ├── Common/
│   ├── Core/
│   ├── Auth/
│   ├── Payload/
│   ├── Persistence/
│   ├── Event_Task/
│   ├── Cache/
│   ├── Session_Context/
│   ├── Policy_Enforcement/
│   ├── Storage_Access/
│   ├── Audit_Observe/
│   ├── Assets/
│   └── Development_Docs/
├── Capability_Modules/
│   ├── Principal_Module/
│   ├── Access_Activation_Module/
│   ├── Account_Module/
│   ├── Order_Module/
│   ├── Payment_Module/
│   ├── Notification_Module/
│   ├── File_Module/
│   └── AI_Module/
├── Client_Applications/
│   └── Unified_Portal/
│       ├── Common/
│       ├── Core/
│       ├── Assets/
│       ├── Channels/
│       │   ├── Web/
│       │   ├── Mobile_H5/
│       │   └── Telegram_Mini_App/
│       └── Development_Docs/
├── Integration_Adapters/
│   ├── OpenAPI_Adapter/
│   └── Webhook_Adapter/
├── Infra_Contracts/
│   ├── PostgreSQL/
│   ├── Redis/
│   ├── MongoDB/
│   ├── Kafka/
│   ├── ClickHouse/
│   ├── OpenSearch/
│   └── Object_Storage/
└── Deploy/
```

## 对象根保留子目录
- `Octopus_Hub/`、`Foundation_Bundle/`、`Capability_Modules/*`、`Client_Applications/*`、`Integration_Adapters/*` 当前都默认预留：
  - `Common/`
  - `Core/`
  - `Assets/`
  - `Development_Docs/`
- `Common/`、`Core/` 是对象内部角色目录，不得在名字里重复对象名。
- `Foundation_Bundle` 的一级能力目录固定采用 `Auth/`、`Payload/`、`Persistence/`、`Event_Task/`、`Cache/`、`Session_Context/`、`Policy_Enforcement/`、`Storage_Access/`、`Audit_Observe/`；不得继续使用 `*_Runtime/` 作为对象级目录后缀。
- `Development_Docs/` 归当前对象自己所有；它不是上层容器的公共 docs 根，也不是要求再嵌一层对象同名目录的冗余壳。
- 因此 `Client_Applications/Unified_Portal/Development_Docs/` 表示 `Unified_Portal` 自己的开发文档容器；只完成项目结构初始化时，该目录默认应为空。
- 若后续进入具体开发闭环，才允许在该容器下继续创建工作主题目录，例如 `<module_dir>/mother_doc/...`；这里的 `<module_dir>` 是开发主题名，不是再次重复 `Unified_Portal`。

## 目录职责
- `Mother_Doc/`
  - 承载项目级母文档、规划、阶段证据与架构叙述。
- `System_Manifests/`
  - 承载全局注册、模块清单、部署矩阵、项目级技术基线与 lint 上游配置。
- `Octopus_Hub/`
  - 承载系统脑子，只管路由、注册、编排、生命周期与健康聚合。
- `Foundation_Bundle/`
  - 承载系统级必需底座能力，是所有业务链路的公共执行底座。
- `Capability_Modules/*`
  - 承载可插拔业务模块；每个模块是一个完整对象。
- `Client_Applications/*`
  - 承载面向人类用户的客户端应用对象；前端对象归这里，而不是归中枢或旧的 `Entry_Objects`。
- `Integration_Adapters/*`
  - 承载对外协议、事件或回调接入对象。
- `Infra_Contracts/*`
  - 承载外部基础设施的接入合同、依赖声明和占位说明，不承载应用域代码。
- `Deploy/`
  - 承载 Compose、容器编排、环境模板与部署相关固定工件。

## 旧目录映射裁决
- `Identity_Service` -> `Capability_Modules/Principal_Module/`
- `Access_Service` / `Access_Activation_Service` -> `Capability_Modules/Access_Activation_Module/`
- `Account_Service` -> `Capability_Modules/Account_Module/`
- `Order_Service` -> `Capability_Modules/Order_Module/`
- `Payment_Service` -> `Capability_Modules/Payment_Module/`
- `Notification_Service` -> `Capability_Modules/Notification_Module/`
- `File_Service` -> `Capability_Modules/File_Module/`
- `AI_Service` -> `Capability_Modules/AI_Module/`
- `Admin_UI` / `User_UI` / unified frontend shell -> `Client_Applications/Unified_Portal/`
- `OpenAPI_Gateway` / `API_Adapter` -> `Integration_Adapters/OpenAPI_Adapter/`
- `Webhook_Receiver` / `Webhook_Adapter` -> `Integration_Adapters/Webhook_Adapter/`
- `Postgres_DB` -> `Infra_Contracts/PostgreSQL/`
- `Redis_Cache` -> `Infra_Contracts/Redis/`
- `Mongo_DB` -> `Infra_Contracts/MongoDB/`
- `MQ_Broker` / `Kafka_Broker` -> `Infra_Contracts/Kafka/`
- `Analytics_DB` / `ClickHouse_DB` -> `Infra_Contracts/ClickHouse/`
- `Search_Engine` / `OpenSearch_Service` -> `Infra_Contracts/OpenSearch/`
- `Object_Storage` -> `Infra_Contracts/Object_Storage/`

## 根目录门禁
- 根目录不再允许直接新增新的 `*_Service`、`*_UI`、`*_DB`、`*_Cache`、`MQ_Broker`、`API_Gateway` 风格目录。
- 任何新增对象必须先归类到 `Octopus_Hub`、`Foundation_Bundle`、`Capability_Modules`、`Client_Applications`、`Integration_Adapters`、`Infra_Contracts` 六大对象区之一，再写入仓库。
