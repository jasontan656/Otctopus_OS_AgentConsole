---
doc_id: dev_projectstructure_constitution.project_structure.capability_module_hotplug_contract
doc_type: topic_atom
topic: Capability-module hot-plug contract for OctopusOS
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends module and hot-plug questions here.
- target: FOUNDATION_CAPABILITY_BUNDLE_BOUNDARY.md
  relation: pairs_with
  direction: lateral
  reason: Foundation bundles are a special case of capability modules.
---

# Capability Module Hotplug Contract

## 技能本体
- 章鱼OS中的能力对象应优先被建模为可插拔模块或可插拔客户端/适配对象，而不是塞回某个抽象中枢目录里的散装代码。
- 热插拔指的是“有合同地接入、启用、停用、移除”，不是随意拔掉。

## 规则说明
- 每个能力模块都应至少具备：
  - `provides`
  - `requires`
  - `health`
  - `degrade_policy`
  - `lifecycle`
- 每个可插拔对象在项目中的固定根目录应放置一个项目级 manifest 文件，推荐固定名为 `module.yaml`。
- `module.yaml` 至少声明：
  - `object_name`
  - `object_type`
  - `provides`
  - `requires`
  - `deployment_unit`
  - `healthcheck`
  - `degrade_policy`
  - `owner_skill`
- 跨对象接入判定应根据 `Development_Docs/` 的项目级合同和对象级 manifest 判断：
  - 能否接入
  - 能否启动
  - 去掉后哪些能力退化
  - 去掉后是否仍可维持系统部分可用
- 非底座对象默认都应允许被移除；只是移除代价可能不同。
- 模块的“可插拔”优先是逻辑能力上的可插拔，不强制要求第一天就拆成独立容器。
- 若某模块去掉后只影响部分能力，它应被定义为非核心模块。
- 若某模块去掉后导致整个系统失效，它应被收敛为 `Foundation_Bundle` 内的系统级必需能力，或被重新裁决为当前阶段不可拔的底座对象，而不是再引入独立 `Octopus_Hub` 根。
- 当前阶段的热插拔优先级裁决为：
  - `Foundation_Bundle`：定义为系统级必需 bundle；停掉等于所有业务链路失效。
  - `Foundation_Bundle/Domain_Modules/*`：默认可拔；拔掉后仅影响所属业务能力。
  - `Client_Applications/*`：默认可拔；拔掉后只影响对应人类交互入口，不改变系统中枢和业务模块本体。
  - `Foundation_Bundle/Integration_Adapters/*`：默认可拔；拔掉后只影响对应外部协议或事件接入通道。
  - `Foundation_Bundle/Infra_Contracts/*`：是否可拔取决于上游依赖，但它们永远不是系统控制面对象。
