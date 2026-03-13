---
doc_id: functional_humenworkzone_manager.routing.task_routing
doc_type: routing_doc
topic: Route readers by Human_Work_Zone management intent
anchors:
- target: ../../SKILL.md
  relation: implements
  direction: upstream
  reason: The skill facade routes Human_Work_Zone tasks into this first routing document.
- target: ../governance/SKILL_DOCSTRUCTURE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Doc-structure policy remains the mandatory governance branch.
- target: ../runtime/OPEN_SOURCE_PROJECTS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Open-source project management is now a stable branch of this skill.
- target: ../runtime/BACKUP_MANAGEMENT_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Backup management is a second stable branch of this skill.
- target: ../runtime/OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Open-source project analysis is a third stable branch of this skill.
- target: ../runtime/BOOKS_AND_READINGS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Books and readings management is a fourth stable branch of this skill.
---

# Task Routing

## 当前分叉轴线
- 本文只按“Human_Work_Zone 管理意图”分流，不扩到整个 workspace。

## 分支一：先锁定目录范围
- 默认受管目录是 `/home/jasontan656/AI_Projects/Human_Work_Zone`。
- 先读 `../governance/SKILL_EXECUTION_RULES.md`，确认本技能当前只管理这个目录本身。

## 分支二：执行收纳或整理
- 当用户说“收纳”“整理”“归位”“归档”时，先读 `../governance/SKILL_EXECUTION_RULES.md`。
- 当前先使用最小规则集执行，不预设复杂目录法。

## 分支三：管理开源项目集中区
- 当任务涉及 `Human_Work_Zone` 内的开源项目时，先读 `../runtime/OPEN_SOURCE_PROJECTS_ZONE_POLICY.md`。
- 该分支负责开源项目专用文件夹、长期 inventory README 与 legacy repo 的挂钩方式。

## 分支四：拉取新的开源项目回本地
- 当任务涉及 clone、下载、保存开源 repo 到本地时，先读 `../runtime/PULL_OPEN_SOURCE_PROJECT_FLOW.md`。
- 该分支负责命名格式、落位目录与拉取后的第一轮登记动作。

## 分支五：维护 inventory README
- 当任务涉及更新项目清单、补基础作用说明或挂钩项目本体 README 时，先读 `../runtime/OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md`。

## 分支六：给项目目录命名
- 当任务只是在决定项目目录名，或需要核对 `<项目名>_<2-3word加强>` 规则时，先读 `../runtime/OPEN_SOURCE_PROJECT_NAMING_RULE.md`。

## 分支七：管理备份集中区
- 当任务涉及备份目录、备份列表或备份收纳时，先读 `../runtime/BACKUP_MANAGEMENT_ZONE_POLICY.md`。
- 该分支负责备份承载目录、备份 README 与备份区的长期目标形态。

## 分支八：执行文件夹备份
- 当用户直接说“把某某文件夹备份”时，先读 `../runtime/CREATE_FOLDER_BACKUP_FLOW.md`。
- 该分支负责整目录复制、固定命名与落备份区后的登记动作。

## 分支九：维护备份清单 README
- 当任务涉及更新备份列表、补一句描述或删除失效备份条目时，先读 `../runtime/BACKUP_README_MAINTENANCE_FLOW.md`。

## 分支十：给备份目录命名
- 当任务需要决定备份目录名，或核对 `<2个word>_bak_<日期>` 规则时，先读 `../runtime/BACKUP_NAMING_RULE.md`。

## 分支十一：管理开源项目分析区
- 当任务涉及开源项目问题分析、报告归档、证据沉淀时，先读 `../runtime/OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md`。
- 该分支负责分析承载目录、按项目归类与分析总 README 的长期目标形态。

## 分支十二：回答开源项目问题并写报告
- 当用户针对某个开源项目突然提问，需要去项目里找答案并沉淀报告时，先读 `../runtime/ANSWER_OPEN_SOURCE_PROJECT_QUESTION_FLOW.md`。
- 该分支负责问题上下文、结论、证据与写回报告。

## 分支十三：维护分析索引 README
- 当任务涉及补分析清单、补项目级索引或更新最新报告入口时，先读 `../runtime/PROJECT_ANALYSIS_INDEX_MAINTENANCE_FLOW.md`。

## 分支十四：核对分析报告结构
- 当任务需要判断一份报告是否“有头有尾、证据完整”时，先读 `../runtime/PROJECT_ANALYSIS_REPORT_STRUCTURE.md`。

## 分支十五：管理书籍与阅读物集中区
- 当任务涉及书籍、阅读资料、读书笔记或网页阅读物时，先读 `../runtime/BOOKS_AND_READINGS_ZONE_POLICY.md`。
- 该分支负责书籍区承载目录、统一命名与根 README 导航。

## 分支十六：执行书籍迁移与整理
- 当任务涉及把一批书籍或阅读资料迁入书籍区时，先读 `../runtime/ORGANIZE_BOOKS_AND_READINGS_FLOW.md`。
- 该分支负责迁移、重命名和资料包落位。

## 分支十七：维护书籍导航 README
- 当任务涉及补书目、更新导航或同步最新命名时，先读 `../runtime/BOOK_LIBRARY_README_MAINTENANCE_FLOW.md`。

## 分支十八：核对书籍命名
- 当任务需要决定书籍或阅读资料的统一名字时，先读 `../runtime/BOOK_NAMING_RULE.md`。
