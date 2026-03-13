---
doc_id: meta_rootfile_manager.assets_managed_targets_ai_projects_octopus_os_readme_md_governed_external
doc_type: topic_atom
topic: Octopus_OS
anchors:
- target: ../../../../SKILL.md
  relation: implements
  direction: upstream
  reason: This document belongs to the governed skill tree under the main facade.
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

当前固定前端对象为 `Client_Applications/Unified_Portal/`，其内部按 `Channels/Web/`、`Channels/Mobile_H5/`、`Channels/Telegram_Mini_App/` 分区。

所有可部署对象根目录都预留：
- `<Object_Name>_Common/`
- `<Object_Name>_Core/`
- `Assets/`
- `Development_Docs/`

旧的 `Entry_Objects/`、`Admin_Portal`、`User_Portal`、`Identity_Module`、`RabbitMQ` 目录语义已经废止，不再作为项目结构依据。
