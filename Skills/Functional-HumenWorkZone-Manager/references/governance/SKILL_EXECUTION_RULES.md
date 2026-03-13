---
doc_id: functional_humenworkzone_manager.governance.execution_rules
doc_type: topic_atom
topic: Execution rules for Human_Work_Zone management tasks
anchors:
- target: SKILL_DOCSTRUCTURE_POLICY.md
  relation: pairs_with
  direction: lateral
  reason: Execution rules and doc-structure policy should stay aligned.
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends Human_Work_Zone tasks here for concrete rules.
- target: ../runtime/OPEN_SOURCE_PROJECTS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Open-source project handling needs a dedicated governed branch.
---

# Skill Execution Rules

## 本地目的
- 本文承载 `Human_Work_Zone` 的最小执行规则，不扩写其他目录治理。

## 当前边界
- 当前只治理 `/home/jasontan656/AI_Projects/Human_Work_Zone`。
- 当前先把“使用这个技能”解释为：把任务范围固定到该目录，再执行收纳、整理、归类或归位。
- `Human_Work_Zone/Open_Source_Projects` 是开源项目集中管理区。
- 开源项目相关动作必须优先落到集中管理区规则，不再把“开源 repo 随手散放”视为目标形态。

## 局部规则
- 若用户明确点名 `Functional-HumenWorkZone-Manager`，默认不要越过 `Human_Work_Zone` 去操作其他目录。
- 若用户只是说“整理一下这个文件夹”，默认这里的“这个文件夹”就是 `Human_Work_Zone`。
- 若任务涉及开源项目，至少要同步考虑：
  - 集中管理区是否需要变更
  - inventory README 是否需要更新
  - 项目目录名是否符合 `<项目名>_<2-3word加强>` 规则
- 现有散落在 `Human_Work_Zone` 根层的开源 repo 视为 legacy placement；先纳入 inventory，再决定是否显式迁移。

## 例外与门禁
- 若用户要求的动作明显超出 `Human_Work_Zone`，应先显式指出范围已经越界。
- 若后续新增专属脚本、清单或规则文档，必须同步更新门面与 routing。
- 若用户没有明确要求，不要直接批量搬迁已存在的本地 repo；优先先建 inventory 与规则，再做显式迁移。

## 下沉执行文档
- 开源项目集中区规则：`../runtime/OPEN_SOURCE_PROJECTS_ZONE_POLICY.md`
- 拉取开源项目流程：`../runtime/PULL_OPEN_SOURCE_PROJECT_FLOW.md`
- inventory README 维护流程：`../runtime/OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md`
- 项目目录命名规则：`../runtime/OPEN_SOURCE_PROJECT_NAMING_RULE.md`
