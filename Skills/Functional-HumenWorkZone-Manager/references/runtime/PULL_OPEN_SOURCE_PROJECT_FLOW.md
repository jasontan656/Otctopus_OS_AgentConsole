---
doc_id: functional_humenworkzone_manager.runtime.pull_open_source_project_flow
doc_type: topic_atom
topic: Flow for pulling an open-source project into Human_Work_Zone
anchors:
- target: OPEN_SOURCE_PROJECTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: Repo intake is one operational branch of the managed zone.
- target: OPEN_SOURCE_PROJECT_NAMING_RULE.md
  relation: requires
  direction: downstream
  reason: A pulled repo needs a compliant local folder name.
- target: OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md
  relation: triggers
  direction: downstream
  reason: Intake must be followed by inventory maintenance.
---

# Pull Open Source Project Flow

## 触发条件
- 当用户要把一个开源项目 clone、下载或保存到 `Human_Work_Zone` 本地时，使用本流程。

## 固定步骤
1. 先确认该项目属于“长期保留的开源项目”，而不是临时试验件。
2. 目标落位目录固定在 `/home/jasontan656/AI_Projects/Human_Work_Zone/Open_Source_Projects/` 下。
3. 本地目录名必须先套用 `OPEN_SOURCE_PROJECT_NAMING_RULE.md`。
4. 拉取完成后，立即更新集中管理区的 `README.md`。
5. 在 `README.md` 里补齐项目基础作用，并挂上指向该项目本体 `README.md` 的链接。

## 最小落地要求
- 不能把新拉取的开源 repo 直接散放在 `Human_Work_Zone` 根层。
- 不能只拉 repo 不补 inventory。
- 若项目本体缺 `README.md`，应在 inventory 中显式标注“upstream README 缺失”。
