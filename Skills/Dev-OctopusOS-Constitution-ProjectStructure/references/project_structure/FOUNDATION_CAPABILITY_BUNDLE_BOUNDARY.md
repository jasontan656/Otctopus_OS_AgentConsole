---
doc_id: "dev_octopusos_constitution_projectstructure.project_structure.foundation_capability_bundle_boundary"
doc_type: "topic_atom"
topic: "Boundary of the always-on foundation capability bundle in OctopusOS"
anchors:
  - target: "CAPABILITY_MODULE_HOTPLUG_CONTRACT.md"
    relation: "pairs_with"
    direction: "lateral"
    reason: "The foundation bundle is governed as a special module bundle."
  - target: "FOLDER_CONTAINER_PLANNING_RULES.md"
    relation: "supports"
    direction: "downstream"
    reason: "Bundle boundaries affect folder and container planning."
---

# Foundation Capability Bundle Boundary

## 技能本体
- 章鱼OS允许存在一个“底座能力层”作为常驻 bundle，一起部署、一起运行、一起服务于业务向内容。
- 这个 bundle 的存在目的是提供所有业务对象必经的底层能力路径，而不是制造新的巨型中枢。

## 规则说明
- 底座能力 bundle 可承载的典型子能力包括：
  - payload normalize / contract reshape
  - persistence access contract
  - queue / worker execution path
  - cache / storage access contract
  - audit / logging / trace context
- 即便当前阶段物理上打成一个 bundle，也必须在逻辑上保留各子能力的边界。
- 若未来需要拆分，拆分的前提不应是重做语义，而应是把已有能力边界物理外显。
- 底座能力 bundle 不等于中枢：
  - 中枢负责“控制与编排”
  - 底座 bundle 负责“公共底层能力执行”
- 若当前项目阶段明确把某些底座能力视为系统级必需，则这些能力可以被定义为常驻且默认一起运行。
