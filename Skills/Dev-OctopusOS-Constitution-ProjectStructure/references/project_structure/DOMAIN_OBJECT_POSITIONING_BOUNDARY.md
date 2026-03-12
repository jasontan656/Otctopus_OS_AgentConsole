---
doc_id: "dev_octopusos_constitution_projectstructure.project_structure.domain_object_positioning_boundary"
doc_type: "topic_atom"
topic: "Project-level positioning boundary for domain objects inside OctopusOS"
anchors:
  - target: "OCTOPUS_OS_HUB_POSITIONING_MODEL.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "Object positioning refines the hub model."
  - target: "FOLDER_CONTAINER_PLANNING_RULES.md"
    relation: "supports"
    direction: "downstream"
    reason: "Folder and container planning depends on object classification."
---

# Domain Object Positioning Boundary

## 技能本体
- 本文只回答“某个对象在章鱼OS里算什么”，不回答“它内部怎么实现”。
- 一个域对象进入章鱼OS前，必须先完成项目级定位，才能进入域内设计。

## 规则说明
- 项目级对象默认只分五类：
  - 中枢对象
  - 底座能力模块
  - 业务能力模块
  - 入口/适配层对象
  - 外部基础设施对象
- 章鱼OS当前阶段的固定对象归属如下：
  - 中枢对象：
    - `Octopus_Hub`
  - 底座能力模块：
    - `Foundation_Bundle`
  - 业务能力模块：
    - `Identity_Module`
    - `Account_Module`
    - `Order_Module`
    - `Payment_Module`
    - `Notification_Module`
    - `File_Module`
    - `AI_Module`
  - 入口/适配层对象：
    - `Admin_Portal`
    - `User_Portal`
    - `OpenAPI_Adapter`
    - `Webhook_Adapter`
  - 外部基础设施对象：
    - `PostgreSQL`
    - `Redis`
    - `RabbitMQ`
    - `Object_Storage`
- 前端在章鱼OS中的定位：
  - 当前固定归为入口/适配层对象，而不是中枢或底座 bundle。
  - 它在系统中的插拔、依赖和中枢关系归本技能治理。
  - 它内部的页面、组件、showroom、状态管理与具体前端规范不归本技能治理。
- 后端域模块在章鱼OS中的定位：
  - 作为完整业务对象接在中枢上。
  - 它是否再内部分层、如何分层，由后端域技能决定。
- 数据库、消息队列、缓存等对象在章鱼OS中的定位：
  - 默认属于外部基础设施对象或底座能力 bundle 的依赖对象。
  - 它们本身不是“中枢的一部分”，只是中枢与模块可依赖的能力来源。
- 旧命名中的 `*_Service`、`*_UI`、`API_Gateway`、`*_DB`、`*_Cache`、`MQ_Broker` 不再是当前项目结构的权威对象名。
- 任何未来新增对象都必须先判断自己属于五类中的哪一类，再决定落在：
  - `Octopus_Hub/`
  - `Foundation_Bundle/`
  - `Capability_Modules/`
  - `Entry_Objects/`
  - `Infra_Contracts/`
- 任何对象若未先完成项目级定位，不应直接进入目录规划、容器命名或 lint 规则沉淀。
