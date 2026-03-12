---
doc_id: "dev_octopusos_constitution_projectstructure.project_structure.octopus_os_target_folder_layout"
doc_type: "topic_atom"
topic: "Concrete target folder layout for the Octopus_OS repository"
anchors:
  - target: "FOLDER_CONTAINER_PLANNING_RULES.md"
    relation: "implements"
    direction: "upstream"
    reason: "This document materializes the folder and container planning rules."
  - target: "DOMAIN_OBJECT_POSITIONING_BOUNDARY.md"
    relation: "requires"
    direction: "upstream"
    reason: "The concrete layout follows the declared object classification."
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
├── System_Manifests/
├── Octopus_Hub/
├── Foundation_Bundle/
├── Capability_Modules/
│   ├── Identity_Module/
│   ├── Account_Module/
│   ├── Order_Module/
│   ├── Payment_Module/
│   ├── Notification_Module/
│   ├── File_Module/
│   └── AI_Module/
├── Entry_Objects/
│   ├── Admin_Portal/
│   ├── User_Portal/
│   ├── OpenAPI_Adapter/
│   └── Webhook_Adapter/
├── Infra_Contracts/
│   ├── PostgreSQL/
│   ├── Redis/
│   ├── RabbitMQ/
│   └── Object_Storage/
└── Deploy/
```

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
- `Entry_Objects/*`
  - 承载对外入口与接入适配对象；前端对象归这里，不归中枢。
- `Infra_Contracts/*`
  - 承载外部基础设施的接入合同、依赖声明和占位说明，不承载应用域代码。
- `Deploy/`
  - 承载 Compose、容器编排、环境模板与部署相关固定工件。

## 旧目录映射裁决
- `AI_Service` -> `Capability_Modules/AI_Module/`
- `Account_Service` -> `Capability_Modules/Account_Module/`
- `File_Service` -> `Capability_Modules/File_Module/`
- `Identity_Service` -> `Capability_Modules/Identity_Module/`
- `Notification_Service` -> `Capability_Modules/Notification_Module/`
- `Order_Service` -> `Capability_Modules/Order_Module/`
- `Payment_Service` -> `Capability_Modules/Payment_Module/`
- `Admin_UI` -> `Entry_Objects/Admin_Portal/`
- `User_UI` -> `Entry_Objects/User_Portal/`
- `API_Gateway` -> 废止为独立顶层对象；中枢路由职责收敛到 `Octopus_Hub/`
- `Postgres_DB` -> `Infra_Contracts/PostgreSQL/`
- `Redis_Cache` -> `Infra_Contracts/Redis/`
- `MQ_Broker` -> `Infra_Contracts/RabbitMQ/`
- `Object_Storage` -> `Infra_Contracts/Object_Storage/`

## 根目录门禁
- 根目录不再允许直接新增新的 `*_Service`、`*_UI`、`*_DB`、`*_Cache`、`MQ_Broker`、`API_Gateway` 风格目录。
- 任何新增对象必须先归类到 `Octopus_Hub`、`Foundation_Bundle`、`Capability_Modules`、`Entry_Objects`、`Infra_Contracts` 五大对象区之一，再写入仓库。
