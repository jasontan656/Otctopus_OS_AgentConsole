---
doc_id: dev_octopusos_constitution_projectstructure.project_structure.folder_container_planning_rules
doc_type: topic_atom
topic: Folder and deployment-container planning rules for OctopusOS
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends folder and container planning questions here.
- target: DOMAIN_OBJECT_POSITIONING_BOUNDARY.md
  relation: requires
  direction: upstream
  reason: Planning folders and containers depends on object classification.
- target: OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md
  relation: supports
  direction: downstream
  reason: This planning rule is materialized by the concrete target folder layout.
---

# Folder Container Planning Rules

## 技能本体
- 目录规划与容器规划是项目级对象边界的落盘形式，不能脱离对象分类单独设计。
- 先问“这是哪类对象”，再问“放在哪个文件夹、用几个容器、怎么部署”。

## 规则说明
- 默认先按逻辑对象规划目录，再按运行时需要决定是否拆成独立容器。
- 推荐的项目级目录视角至少区分：
  - 中枢对象
  - 底座能力 bundle
  - 业务模块对象
  - 客户端应用对象
  - 集成适配对象
  - 外部基础设施或其合同文档
- 当前章鱼OS的顶层文件夹只允许使用以下权威分类目录：
  - `Octopus_Hub/`
  - `Foundation_Bundle/`
  - `Capability_Modules/`
  - `Client_Applications/`
  - `Integration_Adapters/`
  - `Infra_Contracts/`
  - `System_Manifests/`
  - `Deploy/`
  - `Mother_Doc/`
- 容器规划优先按运行职责区分，而不是按代码细枝末节区分。
- 当前默认部署单元固定为：
  - `octopus-hub`
  - `foundation-bundle-api`
  - `foundation-bundle-worker`
  - `capability-<module-name>`
  - `client-application-<object-name>`
  - `integration-adapter-<object-name>`
  - `postgresql`
  - `redis`
  - `mongodb`
  - `kafka`
  - `clickhouse`
  - `opensearch`
  - `object-storage`
- 若一个对象当前要整体插拔，它可以先作为一个完整容器或 bundle 部署单元存在。
- 若一个对象当前只需要逻辑边界，不需要独立扩缩容或独立故障隔离，则可以先与相邻对象同部署，但目录边界不得消失。
- `API_Gateway`、`*_Service`、`*_UI`、`*_DB`、`*_Cache`、`MQ_Broker` 这类旧顶层目录名不再允许继续作为权威目录名存在。
- 每个服务/模块对象根目录至少应承载：
  - `README.md`
  - 若当前对象确实需要项目级身份注册，再按对象类型放置一个对象级 manifest：
    - `hub_manifest.yaml`
    - `module_manifest.yaml`
    - `entry_manifest.yaml`
- 当前阶段 `Foundation_Bundle/` 暂不再要求 bundle 级对象 manifest。
- 当前阶段的服务/模块对象根目录默认只预留以下稳定子目录：
  - `Development_Docs/`
- `Development_Docs/` 是当前阶段唯一允许由项目结构层预置的对象级固定子目录；除此之外，不应再默认预置 `Assets/`、`Channels/` 或其他高抽象内部骨架。
- 对象内部目录命名必须服从单层单义：
  - 对象根只表达对象身份。
  - 一级子目录只表达真实能力边界或真实对象职责。
  - `runtime`、`worker`、`api`、`construction_plan`、`acceptance` 这类运行态或流程态，默认不作为对象级命名后缀。
- 若某个一级目录未来可能独立迁移到别的服务器、扩容单元或部署对象，它应在项目结构层直接以能力名出现，而不是先躲进 `Common/`、`Core/` 这类抽象壳。
- `Development_Docs/` 是“当前服务/模块对象自己的开发文档容器”，不是上层分类容器的共享文档区，也不是要求在对象自己的 `Development_Docs/` 下再套一层对象名或主题名的占位壳。
- 例如 `Client_Applications/Unified_Portal/Development_Docs/` 表示 `Unified_Portal` 这个客户端应用对象自己的开发文档容器；`Foundation_Bundle/Auth/Development_Docs/` 表示 `Auth` 这个底座能力对象自己的开发文档容器。
- `Foundation_Bundle` 是底座能力容器，不再承载共享 `Development_Docs/`；底座能力目录应直接使用能力名，如 `Auth/`、`Payload/`、`Persistence/`，并把各自开发文档落在各自对象根下的 `Development_Docs/`。
- 对象内部具体是否再生长出 `src/`、`tests/`、`deploy/`、`docs/` 或更多域内分层，由对应域技能或实现阶段决定，但不允许越过项目级根目录边界乱放。
- 未来 lint 的作用不是替 AI 设计架构，而是检查目录、对象归属和容器命名是否违反本技能已经声明的项目级结构合同。
