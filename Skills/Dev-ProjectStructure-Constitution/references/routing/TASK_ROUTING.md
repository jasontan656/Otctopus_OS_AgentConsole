---
doc_id: dev_projectstructure_constitution.routing.task_routing
doc_type: routing_doc
topic: Route readers by OctopusOS project-structure task intent
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The facade routes project-structure questions into this task router.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Structure policy remains the mandatory governance branch.
---

# Task Routing

## 当前分叉轴线
- 本文只按“章鱼OS项目结构任务意图”分流，不处理域内实现细节。

## 分支一：问项目整体定位与中枢边界
- 先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 再读 `../project_structure/OCTOPUS_OS_HUB_POSITIONING_MODEL.md`。
- 若问题涉及“某域在章鱼OS里算什么对象”，再补 `../project_structure/DOMAIN_OBJECT_POSITIONING_BOUNDARY.md`。

## 分支二：问模块插拔、依赖关系与底座能力
- 先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 再读 `../project_structure/CAPABILITY_MODULE_HOTPLUG_RULES.md`。
- 若问题涉及“哪些能力可以作为常驻底座 bundle 一起部署”，再补 `../project_structure/FOUNDATION_CAPABILITY_BUNDLE_BOUNDARY.md`。
- 若问题涉及“当前阶段技术选型已经定成什么”，再补 `../project_structure/PROJECT_TECHSTACK_BASELINE.md`。

## 分支三：问目录、容器与部署对象规划
- 先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 再读 `../project_structure/FOLDER_CONTAINER_PLANNING_RULES.md`。
- 再读 `../project_structure/OCTOPUS_OS_TARGET_FOLDER_LAYOUT.md`。
- 若问题同时涉及对象归属，再补 `../project_structure/DOMAIN_OBJECT_POSITIONING_BOUNDARY.md`。
- 若问题同时涉及各目录承载的技术对象，再补 `../project_structure/PROJECT_TECHSTACK_BASELINE.md`。
