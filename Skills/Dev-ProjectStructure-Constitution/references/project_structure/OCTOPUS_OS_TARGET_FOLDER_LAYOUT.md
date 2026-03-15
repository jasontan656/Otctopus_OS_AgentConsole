---
doc_id: dev_projectstructure_constitution.project_structure.octopus_os_target_folder_layout
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
├── Development_Docs/
│   ├── README.md
│   ├── AGENTS.md
│   ├── graph/
│   └── mother_doc/
├── Client_Applications/
│   ├── README.md
│   ├── entry_manifest.yaml
│   ├── package.json
│   ├── src/
│   ├── scripts/
│   ├── tests/
│   └── runtime_artifacts/
├── Foundation_Bundle/
│   ├── README.md
│   ├── Auth/
│   │   └── Development_Docs/
│   ├── Payload/
│   │   └── Development_Docs/
│   ├── Persistence/
│   │   └── Development_Docs/
│   ├── Event_Task/
│   │   └── Development_Docs/
│   ├── Cache/
│   │   └── Development_Docs/
│   ├── Session_Context/
│   │   └── Development_Docs/
│   ├── Policy_Enforcement/
│   │   └── Development_Docs/
│   ├── Storage_Access/
│   │   └── Development_Docs/
│   ├── Audit_Observe/
│   │   └── Development_Docs/
│   ├── Domain_Modules/
│   │   ├── Principal_Module/
│   │   │   └── Development_Docs/
│   │   ├── Access_Activation_Module/
│   │   │   └── Development_Docs/
│   │   ├── Account_Module/
│   │   │   └── Development_Docs/
│   │   ├── Order_Module/
│   │   │   └── Development_Docs/
│   │   ├── Payment_Module/
│   │   │   └── Development_Docs/
│   │   ├── Notification_Module/
│   │   │   └── Development_Docs/
│   │   ├── File_Module/
│   │   │   └── Development_Docs/
│   │   └── AI_Module/
│   │       └── Development_Docs/
│   ├── Integration_Adapters/
│   │   ├── OpenAPI_Adapter/
│   │   │   └── Development_Docs/
│   │   └── Webhook_Adapter/
│   │       └── Development_Docs/
│   └── Infra_Contracts/
│       ├── PostgreSQL/
│       │   └── Development_Docs/
│       ├── Redis/
│       │   └── Development_Docs/
│       ├── MongoDB/
│       │   └── Development_Docs/
│       ├── Kafka/
│       │   └── Development_Docs/
│       ├── ClickHouse/
│       │   └── Development_Docs/
│       ├── OpenSearch/
│       │   └── Development_Docs/
│       └── Object_Storage/
│           └── Development_Docs/
└── Deploy_Guide/
    └── README.md
```

## 对象根保留子目录
- `Foundation_Bundle/*`、`Foundation_Bundle/Domain_Modules/*`、`Foundation_Bundle/Integration_Adapters/*`、`Foundation_Bundle/Infra_Contracts/*` 当前默认只预留：
  - `Development_Docs/`
- `Client_Applications/` 当前是单一前端实现根，不再额外预置 `Unified_Portal/` 二级对象壳，也不再在其下预置 `Development_Docs/`。
- 不再默认预置 `Common/`、`Core/` 这类高抽象角色目录；若没有真实能力语义，就不应在项目结构层先长出内部骨架。
- `Foundation_Bundle` 的平台能力目录固定采用 `Auth/`、`Payload/`、`Persistence/`、`Event_Task/`、`Cache/`、`Session_Context/`、`Policy_Enforcement/`、`Storage_Access/`、`Audit_Observe/`；不得继续使用 `*_Runtime/` 作为对象级目录后缀。
- 这些平台能力目录代表后端根内未来可独立演化、独立扩容或独立拆部署的能力对象，而不是 bundle 内部的抽象层分区。
- `Foundation_Bundle/` 本身不承载共享 `Development_Docs/`；开发文档一律下沉到各后端对象自己的 `Development_Docs/`。
- `Development_Docs/` 归当前服务/模块对象自己所有；它不是上层容器的公共 docs 根，也不是要求再嵌一层对象同名目录的冗余壳。
- 章鱼OS当前的单一前端产品文档例外地集中收敛在 repo 根 `Development_Docs/`；`Foundation_Bundle/Domain_Modules/Principal_Module/Development_Docs/` 则表示 `Principal_Module` 自己的开发文档容器。
- 章鱼OS当前阶段不再把 `Channels/`、`Assets/` 视为项目结构层的权威预置子目录；若未来需要这些域内目录，应由对应域技能在对象内部实现阶段决定。

## 目录职责
- `Development_Docs/`
  - 承载项目级开发文档、架构说明、当前单一前端产品的 mother_doc/graph/runtime 资产与 repo 级证据入口。
- `Client_Applications/`
  - 直接承载面向人类用户的前端实现根；当前单一客户端产品语义 `Unified_Portal` 物理上收敛在这里，而不是再嵌套一个对象目录。
- `Foundation_Bundle/`
  - 作为后端根容器，统一承载平台能力对象、业务模块、集成适配对象与基础设施接入合同。
- `Foundation_Bundle/Domain_Modules/*`
  - 承载可插拔业务模块；每个模块是一个完整后端对象。
- `Foundation_Bundle/Integration_Adapters/*`
  - 承载对外协议、事件或回调接入对象。
- `Foundation_Bundle/Infra_Contracts/*`
  - 承载外部基础设施的接入合同、依赖声明和占位说明，不承载应用域代码。
- `Deploy_Guide/`
  - 承载部署脚本、环境模板、门禁、CI 与上线说明。

## 旧目录映射裁决
- `System_Manifests/` -> `Development_Docs/`
- `Deploy/` -> `Deploy_Guide/`
- `Identity_Service` -> `Foundation_Bundle/Domain_Modules/Principal_Module/`
- `Access_Service` / `Access_Activation_Service` -> `Foundation_Bundle/Domain_Modules/Access_Activation_Module/`
- `Account_Service` -> `Foundation_Bundle/Domain_Modules/Account_Module/`
- `Order_Service` -> `Foundation_Bundle/Domain_Modules/Order_Module/`
- `Payment_Service` -> `Foundation_Bundle/Domain_Modules/Payment_Module/`
- `Notification_Service` -> `Foundation_Bundle/Domain_Modules/Notification_Module/`
- `File_Service` -> `Foundation_Bundle/Domain_Modules/File_Module/`
- `AI_Service` -> `Foundation_Bundle/Domain_Modules/AI_Module/`
- `Admin_UI` / `User_UI` / unified frontend shell -> `Client_Applications/`
- `OpenAPI_Gateway` / `API_Adapter` -> `Foundation_Bundle/Integration_Adapters/OpenAPI_Adapter/`
- `Webhook_Receiver` / `Webhook_Adapter` -> `Foundation_Bundle/Integration_Adapters/Webhook_Adapter/`
- `Postgres_DB` -> `Foundation_Bundle/Infra_Contracts/PostgreSQL/`
- `Redis_Cache` -> `Foundation_Bundle/Infra_Contracts/Redis/`
- `Mongo_DB` -> `Foundation_Bundle/Infra_Contracts/MongoDB/`
- `MQ_Broker` / `Kafka_Broker` -> `Foundation_Bundle/Infra_Contracts/Kafka/`
- `Analytics_DB` / `ClickHouse_DB` -> `Foundation_Bundle/Infra_Contracts/ClickHouse/`
- `Search_Engine` / `OpenSearch_Service` -> `Foundation_Bundle/Infra_Contracts/OpenSearch/`
- `Object_Storage` -> `Foundation_Bundle/Infra_Contracts/Object_Storage/`

## 根目录门禁
- 根目录不再允许直接新增新的 `*_Service`、`*_UI`、`*_DB`、`*_Cache`、`MQ_Broker`、`API_Gateway` 风格目录。
- 根目录不再允许恢复 `Mother_Doc/`、`Octopus_Hub/`、`System_Manifests/`、`Capability_Modules/`、`Integration_Adapters/`、`Infra_Contracts/`、`Deploy/` 这类旧顶层目录。
- 任何新增后端对象必须先归类到 `Foundation_Bundle` 内的平台能力对象、`Domain_Modules`、`Integration_Adapters`、`Infra_Contracts` 四类后端区之一，再写入仓库。
- 项目级全局资料若不属于某个对象根，应优先进入 `Development_Docs/`、`Deploy_Guide/` 或仓库根 `README.md`，而不是新开顶层 docs 容器。
