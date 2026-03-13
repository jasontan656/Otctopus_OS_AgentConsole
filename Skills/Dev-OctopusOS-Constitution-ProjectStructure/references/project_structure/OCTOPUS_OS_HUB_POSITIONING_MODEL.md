---
doc_id: dev_octopusos_constitution_projectstructure.project_structure.hub_positioning_model
doc_type: topic_atom
topic: System-level hub positioning model of OctopusOS
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends hub-model questions here.
- target: DOMAIN_OBJECT_POSITIONING_BOUNDARY.md
  relation: pairs_with
  direction: lateral
  reason: The hub model needs object-positioning boundaries to stay precise.
---

# OctopusOS Hub Positioning Model

## 技能本体
- 章鱼OS不是“若干独立服务的松散集合”，而是一个以中枢为核心的模块化系统。
- 中枢是整个系统的脑子，负责全局路由、能力注册、依赖编排、模块启停与全局策略执行。
- 中枢是项目级唯一必需核心对象；中枢失效等价于整个章鱼OS失效。
- 当前中枢对象的固定工程名为 `Octopus_Hub`，其目录根固定为 `Octopus_OS/Octopus_Hub/`。

## 规则说明
- 中枢层只负责项目级控制职责：
  - 路由与编排
  - 模块注册与发现
  - 依赖校验
  - 生命周期管理
  - 全局 feature gating
  - 系统级健康聚合
- 当前阶段 `Octopus_Hub` 的项目级技术基线固定为：
  - `Python 3.12`
  - `FastAPI`
  - `Pydantic v2`
- `Octopus_Hub` 内允许存在的核心子对象仅包括：
  - `Hub_API`
  - `Hub_Router`
  - `Module_Registry`
  - `Dependency_Graph`
  - `Lifecycle_Manager`
  - `Health_Aggregator`
- 中枢不应直接吞并：
  - 具体业务规则
  - 具体数据库 schema
  - 某个域内部的实现细节
  - 某个能力模块内部的私有状态机
- 对外入口应优先接到中枢，再由中枢决定流向哪个模块或能力对象。
- 中枢存在的意义不是“自己做所有事”，而是“让所有对象按统一合同接入与退出系统”。
- `API_Gateway` 不再作为章鱼OS的独立顶层系统对象保留；所有系统级路由中枢职责统一收敛到 `Octopus_Hub`。
