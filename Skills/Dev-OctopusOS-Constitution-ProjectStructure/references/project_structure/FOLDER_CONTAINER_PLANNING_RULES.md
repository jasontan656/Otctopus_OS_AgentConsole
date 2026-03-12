---
doc_id: "dev_octopusos_constitution_projectstructure.project_structure.folder_container_planning_rules"
doc_type: "topic_atom"
topic: "Folder and deployment-container planning rules for OctopusOS"
anchors:
  - target: "../routing/TASK_ROUTING.md"
    relation: "implements"
    direction: "upstream"
    reason: "Task routing sends folder and container planning questions here."
  - target: "DOMAIN_OBJECT_POSITIONING_BOUNDARY.md"
    relation: "requires"
    direction: "upstream"
    reason: "Planning folders and containers depends on object classification."
  - target: "OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md"
    relation: "supports"
    direction: "downstream"
    reason: "This planning rule is materialized by the concrete target folder layout."
---

# Folder Container Planning Rules

## 技能本体
- 目录规划与容器规划是项目级对象边界的落盘形式，不能脱离对象分类单独设计。
- 先问“这是哪类对象”，再问“放在哪个文件夹、用几个容器、怎么部署”。

## 规则说明
- 默认先按逻辑对象规划目录，再按运行时需要决定是否拆成独立容器。
- 推荐的项目级目录视角至少区分：
  - 中枢对象
  - 底座能力 bundle / capability modules
  - 业务模块对象
  - 入口/适配层对象
  - 外部基础设施或其合同文档
- 当前章鱼OS的顶层文件夹只允许使用以下权威分类目录：
  - `Octopus_Hub/`
  - `Foundation_Bundle/`
  - `Capability_Modules/`
  - `Entry_Objects/`
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
  - `entry-<object-name>`
  - `postgresql`
  - `redis`
  - `rabbitmq`
  - `object-storage`
- 若一个对象当前要整体插拔，它可以先作为一个完整容器或 bundle 部署单元存在。
- 若一个对象当前只需要逻辑边界，不需要独立扩缩容或独立故障隔离，则可以先与相邻对象同部署，但目录边界不得消失。
- `API_Gateway`、`*_Service`、`*_UI`、`*_DB`、`*_Cache`、`MQ_Broker` 这类旧顶层目录名不再允许继续作为权威目录名存在。
- 每个对象根目录至少应承载：
  - `README.md`
  - `module.yaml`
- 对象内部具体是否再生长出 `src/`、`tests/`、`deploy/`、`docs/`，由对应域技能或实现阶段决定，但不允许越过项目级根目录边界乱放。
- 未来 lint 的作用不是替 AI 设计架构，而是检查目录、对象归属和容器命名是否违反本技能已经声明的项目级结构合同。
