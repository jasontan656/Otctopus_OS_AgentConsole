---
doc_id: dev_octopusos_constitution_projectstructure.project_structure.capability_module_hotplug_contract
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
- 章鱼OS中的非中枢能力应优先被建模为可插拔模块，而不是中枢内部的散装代码。
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
- 中枢应根据模块合同判断：
  - 能否接入
  - 能否启动
  - 去掉后哪些能力退化
  - 去掉后是否仍可维持系统部分可用
- 非中枢模块默认都应允许被移除；只是移除代价可能不同。
- 模块的“可插拔”优先是逻辑能力上的可插拔，不强制要求第一天就拆成独立容器。
- 若某模块去掉后只影响部分能力，它应被定义为非核心模块。
- 若某模块去掉后导致整个系统失效，它要么是中枢，要么是当前阶段被定义成系统级必需 bundle 的能力。
- 当前阶段的热插拔优先级裁决为：
  - `Octopus_Hub`：不可拔；拔掉等于系统整体失效。
  - `Foundation_Bundle`：定义为系统级必需 bundle；停掉等于所有业务链路失效。
  - `Capability_Modules/*`：默认可拔；拔掉后仅影响所属业务能力。
  - `Client_Applications/*`：默认可拔；拔掉后只影响对应人类交互入口，不改变系统中枢和业务模块本体。
  - `Integration_Adapters/*`：默认可拔；拔掉后只影响对应外部协议或事件接入通道。
  - `Infra_Contracts/*`：是否可拔取决于上游依赖，但它们永远不是中枢对象。
