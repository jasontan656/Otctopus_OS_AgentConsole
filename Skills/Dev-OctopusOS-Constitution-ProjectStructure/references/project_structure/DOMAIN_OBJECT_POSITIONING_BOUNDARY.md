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
- 前端在章鱼OS中的定位：
  - 可以被视为一个完整业务对象或入口对象接入章鱼OS。
  - 它在系统中的插拔、依赖和中枢关系归本技能治理。
  - 它内部的页面、组件、showroom、状态管理与具体前端规范不归本技能治理。
- 后端域模块在章鱼OS中的定位：
  - 作为完整业务对象接在中枢上。
  - 它是否再内部分层、如何分层，由后端域技能决定。
- 数据库、消息队列、缓存等对象在章鱼OS中的定位：
  - 默认属于外部基础设施对象或底座能力 bundle 的依赖对象。
  - 它们本身不是“中枢的一部分”，只是中枢与模块可依赖的能力来源。
- 任何对象若未先完成项目级定位，不应直接进入目录规划、容器命名或 lint 规则沉淀。
