---
doc_id: functional_humenworkzone_manager.runtime.open_source_projects_zone_policy
doc_type: topic_atom
topic: Dedicated open-source project zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends open-source project tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The zone policy must obey the skill execution boundary.
- target: PULL_OPEN_SOURCE_PROJECT_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Pulling a repo into the zone is a separate operational flow.
- target: OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Inventory upkeep is split into its own maintenance flow.
- target: OPEN_SOURCE_PROJECT_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Naming is a distinct rule set for project folders.
---

# Open Source Projects Zone Policy

## 目标目录
- 开源项目集中管理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Open_Source_Projects`。
- 该目录是 `Human_Work_Zone` 下所有“本地保存的开源项目”应当对齐的目标形态入口。

## 目录职责
- 本目录负责承载开源项目 inventory 与后续新拉取 repo 的规范落位。
- 本目录下必须长期维护 `README.md`，记录：
  - 当前有哪些开源项目
  - 每个项目的基础作用
  - 指向项目本体 `README.md` 的内联链接

## legacy 项目处理
- 当前已经散落在 `Human_Work_Zone` 其他位置的开源 repo，先视为 legacy placement。
- 只要某个 legacy repo 被确认属于“长期保留的开源项目”，就应在集中管理区的 `README.md` 里登记。
- 若用户没有显式要求，不自动批量搬迁 legacy repo；先通过 inventory 建立稳定视图。

## 进入本区后的后续分流
- 若要把新开源 repo 拉回本地，进入 `PULL_OPEN_SOURCE_PROJECT_FLOW.md`。
- 若要维护项目清单或说明文字，进入 `OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md`。
- 若要决定目录名或校验命名，进入 `OPEN_SOURCE_PROJECT_NAMING_RULE.md`。
