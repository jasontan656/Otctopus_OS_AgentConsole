---
doc_id: dev_projectstructure_constitution.project_structure.domain_object_positioning_boundary
doc_type: topic_atom
topic: Project-level positioning boundary for domain objects inside OctopusOS
anchors:
- target: FOLDER_CONTAINER_PLANNING_RULES.md
  relation: supports
  direction: downstream
  reason: Folder and container planning depends on object classification.
- target: PROJECT_TECHSTACK_BASELINE.md
  relation: pairs_with
  direction: lateral
  reason: Object positioning and tech ownership must remain aligned.
---

# Domain Object Positioning Boundary

## 技能本体
- 本文只回答“某个对象在章鱼OS里算什么”，不回答“它内部怎么实现”。
- 一个域对象进入章鱼OS前，必须先完成项目级定位，才能进入域内设计。

## 规则说明
- 项目级对象默认只分五类：
  - 后端平台能力对象
  - 业务能力模块
  - 客户端应用对象
  - 集成适配对象
  - 外部基础设施对象
- `Development_Docs/` 与 `Deploy_Guide/` 是 repo 级容器，不属于以上五类中的“对象”；前者承载项目文档与证据，后者承载部署脚本、门禁与 CI。
- 章鱼OS当前阶段的固定对象归属如下：
  - 后端平台能力对象：
    - `Auth`
    - `Payload`
    - `Persistence`
    - `Event_Task`
    - `Cache`
    - `Session_Context`
    - `Policy_Enforcement`
    - `Storage_Access`
    - `Audit_Observe`
  - 业务能力模块：
    - `Principal_Module`
    - `Access_Activation_Module`
    - `Account_Module`
    - `Order_Module`
    - `Payment_Module`
    - `Notification_Module`
    - `File_Module`
    - `AI_Module`
  - 客户端应用对象：
    - `Unified_Portal`（物理实现根收敛在 `Client_Applications/`）
  - 集成适配对象：
    - `OpenAPI_Adapter`
    - `Webhook_Adapter`
  - 外部基础设施对象：
    - `PostgreSQL`
    - `Redis`
    - `MongoDB`
    - `Kafka`
    - `ClickHouse`
    - `OpenSearch`
    - `Object_Storage`
- 前端在章鱼OS中的定位：
  - 当前固定归为客户端应用对象，而不是底座 bundle、集成适配对象或旧的入口混合层。
  - 当前阶段的物理实现根直接收敛在 `Client_Applications/`，不再额外创建 `Client_Applications/Unified_Portal/` 对象壳。
  - 它在系统中的插拔、依赖和跨对象合同关系归本技能治理。
  - 它内部的页面、组件、showroom、状态管理与具体前端规范不归本技能治理。
- 集成适配对象在章鱼OS中的定位：
  - 负责把外部协议、事件或 webhook 合同接入 `Foundation_Bundle` 内的平台能力对象或业务模块。
  - 它们不是客户端应用，也不是某个抽象中枢内部实现。
- 后端域模块在章鱼OS中的定位：
  - 作为完整业务对象下沉在 `Foundation_Bundle/Domain_Modules/` 内，并接在平台能力对象与跨对象 manifest 合同之上。
  - 它是否再内部分层、如何分层，由后端域技能决定。
- 数据库、消息队列、缓存、搜索与分析存储对象在章鱼OS中的定位：
  - 默认属于外部基础设施对象，并下沉在 `Foundation_Bundle/Infra_Contracts/` 内作为后端依赖合同。
  - 它们本身不是“系统脑子的一部分”，只是后端平台能力对象、模块对象或客户端对象可依赖的能力来源。
- 项目级全局说明与证据不再通过顶层 `Mother_Doc/` 或 `System_Manifests/` 定位；它们应落在 `Development_Docs/`、仓库 `README.md` 或拥有该语义的对象 `Development_Docs/`。
- 旧命名中的 `*_Service`、`*_UI`、`API_Gateway`、`*_DB`、`*_Cache`、`MQ_Broker`、`Octopus_Hub`、`Mother_Doc`、`System_Manifests`、`Capability_Modules`、`Integration_Adapters`、`Infra_Contracts`、`Deploy` 不再是当前项目结构的权威对象根或顶层容器名。
- 任何未来新增对象都必须先判断自己属于五类中的哪一类，再决定落在：
  - `Development_Docs/`（仅限项目级文档资料，不作为对象根）
  - `Client_Applications/`
  - `Foundation_Bundle/`
  - `Deploy_Guide/`（仅限部署与门禁资料，不作为对象根）
- 任何对象若未先完成项目级定位，不应直接进入目录规划、容器命名或 lint 规则沉淀。
