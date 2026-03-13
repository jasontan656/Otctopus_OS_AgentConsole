---
owner: "由 `Octopus_OS` repository root container 所代表的 公共说明面 负责；当前通过 `$Meta-RootFile-Manager` 的 `README_MD` 通道受管并同步。"
---
# Octopus_OS

章鱼OS当前采用 `中枢 + 底座 bundle + 业务模块 + 客户端应用 + 集成适配 + 外部基础设施合同` 的项目级结构。

当前阶段的权威顶层目录只有：
- `Mother_Doc/`
- `System_Manifests/`
- `Octopus_Hub/`
- `Foundation_Bundle/`
- `Capability_Modules/`
- `Client_Applications/`
- `Integration_Adapters/`
- `Infra_Contracts/`
- `Deploy/`

当前固定前端对象为 `Client_Applications/Unified_Portal/`；项目结构层当前只固定该对象根与其 `Development_Docs/`，域内前端目录形态下沉到实现阶段决定。

所有服务/模块对象根目录当前只预留一个固定子目录：
- `Development_Docs/`

旧的 `Entry_Objects/`、`Admin_Portal`、`User_Portal`、`Identity_Module`、`RabbitMQ` 目录语义已经废止，不再作为项目结构依据。
