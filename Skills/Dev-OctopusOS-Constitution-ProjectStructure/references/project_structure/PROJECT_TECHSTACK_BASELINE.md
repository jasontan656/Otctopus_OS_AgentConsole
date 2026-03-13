---
doc_id: "dev_octopusos_constitution_projectstructure.project_structure.project_techstack_baseline"
doc_type: "topic_atom"
topic: "Project-level baseline tech stack for OctopusOS"
anchors:
  - target: "FOUNDATION_CAPABILITY_BUNDLE_BOUNDARY.md"
    relation: "supports"
    direction: "upstream"
    reason: "The foundation bundle depends on the declared project tech baseline."
  - target: "OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md"
    relation: "supports"
    direction: "downstream"
    reason: "The target folder layout materializes the declared tech-object placement."
---

# Project Techstack Baseline

## 技能本体
- 本文固定章鱼OS当前阶段的项目级技术选型，并声明这些技术在系统里的对象归属。
- 本文只决定“哪种技术属于哪个项目对象”，不展开这些技术各自的编码细则。

## 固定选型
- 服务端项目级基线：
  - `Python 3.12`
  - `FastAPI`
  - `Pydantic v2`
- 数据访问基线：
  - `SQLAlchemy 2`
  - `Alembic`
- 异步任务基线：
  - `Celery`
- 外部基础设施基线：
  - `PostgreSQL`
  - `Redis`
  - `MongoDB`
  - `Kafka`
  - `ClickHouse`
  - `OpenSearch`
  - `MinIO` / `S3-compatible Object Storage`
- 前端入口对象基线：
  - `Vue 3`
  - `TypeScript`
  - `Vite`
- 部署基线：
  - `Docker`
  - `Docker Compose`
- 可观测性基线：
  - `structlog`
  - `OpenTelemetry`

## 对象归属
- `Octopus_Hub`：
  - 主要承载 `Python 3.12 + FastAPI + Pydantic v2`
  - 作用：提供中枢 API、路由与生命周期控制
- `Foundation_Bundle`：
  - 主要承载 `Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2 + Alembic + Celery + structlog + OpenTelemetry`
  - 作用：提供业务必经的底层执行能力
- `Capability_Modules/*`：
  - 默认沿用服务端项目级基线 `Python 3.12 + FastAPI + Pydantic v2`
  - 是否使用 `SQLAlchemy 2`、`Celery` 等由模块依赖决定，但不得绕过 `Foundation_Bundle` 的项目级合同
- `Client_Applications/Unified_Portal`：
  - 固定承载 `Vue 3 + TypeScript + Vite`
  - 作用：作为章鱼OS面向人类用户的统一客户端应用对象，而不是系统中枢
  - 其内部渠道壳当前固定为 `Channels/Web`、`Channels/Mobile_H5`、`Channels/Telegram_Mini_App`
- `Integration_Adapters/OpenAPI_Adapter` 与 `Integration_Adapters/Webhook_Adapter`：
  - 默认承载服务端项目级基线
  - 作用：把外部协议接入中枢或业务模块
- `Infra_Contracts/*`：
  - 只声明 `PostgreSQL`、`Redis`、`MongoDB`、`Kafka`、`ClickHouse`、`OpenSearch`、`Object_Storage` 在系统中的位置和接入约束
  - 不承载应用层实现代码

## 排除项
- `Nginx`、`Traefik`、`Caddy` 这类边缘代理不是章鱼OS当前阶段的宪法级核心对象；如后续需要接入，应作为 `Deploy/` 或入口适配附属物治理。
- 前端状态管理、UI 组件库、后端内部包管理、测试框架等域内细节，不在本文固定范围内。
