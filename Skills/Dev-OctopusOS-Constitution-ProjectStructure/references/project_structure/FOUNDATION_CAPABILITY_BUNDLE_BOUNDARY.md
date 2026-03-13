---
doc_id: dev_octopusos_constitution_projectstructure.project_structure.foundation_capability_bundle_boundary
doc_type: topic_atom
topic: Boundary of the always-on foundation capability bundle in OctopusOS
anchors:
- target: CAPABILITY_MODULE_HOTPLUG_RULES.md
  relation: pairs_with
  direction: lateral
  reason: The foundation bundle is governed as a special module bundle.
- target: FOLDER_CONTAINER_PLANNING_RULES.md
  relation: supports
  direction: downstream
  reason: Bundle boundaries affect folder and container planning.
---

# Foundation Capability Bundle Boundary

## 技能本体
- 章鱼OS允许存在一个“底座能力层”作为常驻 bundle，一起部署、一起运行、一起服务于业务向内容。
- 这个 bundle 的存在目的是提供所有业务对象必经的底层能力路径，而不是制造新的巨型中枢。
- 当前底座能力层的固定工程名为 `Foundation_Bundle`，其目录根固定为 `Octopus_OS/Foundation_Bundle/`。

## 规则说明
- `Foundation_Bundle` 当前阶段固定包含以下子能力：
  - `Auth`
    - 作用：统一认证、主体校验与身份相关运行时合同。
  - `Payload`
    - 作用：统一 request / response / event payload 的规范化、校验、重塑与出口收口。
  - `Persistence`
    - 作用：统一事务边界、repository adapter、数据库访问合同。
  - `Event_Task`
    - 作用：统一异步任务投递、worker 执行路径、重试与消费通道。
  - `Cache`
    - 作用：统一缓存、热点数据与快速读取合同。
  - `Session_Context`
    - 作用：统一会话态、上下文透传与请求生命周期状态合同。
  - `Policy_Enforcement`
    - 作用：统一鉴权、策略裁决与跨模块执行约束。
  - `Storage_Access`
    - 作用：统一文件与对象存储的访问合同、元数据桥接与下载上传通道。
  - `Audit_Observe`
    - 作用：统一日志上下文、trace、审计线索和系统级观测基线。
- 这些目录名表达的是“底座能力身份”，不是部署形态；`Runtime` 已被视为 bundle 上下文中的默认语义，不应继续出现在对象级物理路径后缀里。
- 这些能力目录的存在意义不是把 bundle 内部做成抽象分层，而是把未来可能独立拆部署、独立扩容、独立服务更多模块的能力边界提前钉死。
- 因此 `Foundation_Bundle` 不应再预置 `Common/`、`Core/` 这类高抽象角色目录，以免覆盖掉原本的“解耦能力模块”语义。
- `Foundation_Bundle` 的项目级技术选型固定为：
  - `Python 3.12`
  - `FastAPI`
  - `Pydantic v2`
  - `SQLAlchemy 2`
  - `Alembic`
  - `Celery`
  - `structlog`
  - `OpenTelemetry`
- `Foundation_Bundle` 的外部基础设施依赖固定为：
  - `PostgreSQL`
  - `Redis`
  - `Kafka`
  - `MongoDB`
  - `ClickHouse`
  - `OpenSearch`
  - `Object_Storage`
- 上述基础设施是 `Foundation_Bundle` 的依赖对象，不属于 `Foundation_Bundle` 目录本体。
- 即便当前阶段物理上打成一个 bundle，也必须在逻辑上保留各子能力的边界。
- 若未来需要拆分，拆分的前提不应是重做语义，而应是把已有能力边界物理外显。
- 底座能力 bundle 不等于中枢：
  - 中枢负责“控制与编排”
  - 底座 bundle 负责“公共底层能力执行”
- 若当前项目阶段明确把某些底座能力视为系统级必需，则这些能力可以被定义为常驻且默认一起运行。
- 当前默认部署裁决为：
  - `Foundation_Bundle` 是一个逻辑 bundle。
  - 默认需要同时启动两个运行单元：
    - `foundation-bundle-api`
    - `foundation-bundle-worker`
  - 两个运行单元缺一不可；任一失效都视为 `Foundation_Bundle` 整体失效。
