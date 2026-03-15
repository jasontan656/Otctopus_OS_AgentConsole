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
- target: ../runtime/BACKUP_MANAGEMENT_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Backup handling needs a dedicated governed branch.
- target: ../runtime/OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Project analysis handling needs a dedicated governed branch.
- target: ../runtime/BOOKS_AND_READINGS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Books and readings handling needs a dedicated governed branch.
- target: ../runtime/TEMPORARY_PROJECTS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Temporary project handling needs a dedicated governed branch.
- target: ../runtime/COMPANY_DOCUMENTS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Company-document handling needs a dedicated governed branch.
- target: ../runtime/EXTERNAL_RESEARCH_REPORTS_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: External research report handling needs a dedicated governed branch.
- target: ../runtime/TEMPORARY_FILES_ZONE_POLICY.md
  relation: routes_to
  direction: downstream
  reason: Temporary file handling needs a dedicated governed branch.
---

# Skill Execution Rules

## 本地目的
- 本文承载 `Human_Work_Zone` 的最小执行规则，不扩写其他目录治理。

## 当前边界
- 当前只治理 `/home/jasontan656/AI_Projects/Human_Work_Zone`。
- 当前先把“使用这个技能”解释为：把任务范围固定到该目录，再执行收纳、整理、归类或归位。
- `Human_Work_Zone/Open_Source_Projects` 是开源项目集中管理区。
- `Human_Work_Zone/Backup_Management` 是备份集中管理区。
- `Human_Work_Zone/Open_Source_Project_Analysis` 是开源项目分析集中区。
- `Human_Work_Zone/Books_and_Readings` 是书籍与阅读物集中管理区。
- `Human_Work_Zone/Temporary_Projects` 是临时项目集中管理区。
- `Human_Work_Zone/Temporary_Files` 是临时文件集中治理区。
- `Human_Work_Zone/Company_Documents` 是公司&文档集中管理区。
- `Human_Work_Zone/External_Research_Reports` 是外部调研报告集中管理区。
- 开源项目相关动作必须优先落到集中管理区规则，不再把“开源 repo 随手散放”视为目标形态。
- 备份相关动作必须优先落到备份区规则，不再把“随手复制一份放任意位置”视为目标形态。
- 开源项目分析相关动作必须优先落到分析区规则，不再把“只在对话里说答案、不留上下文和证据”视为目标形态。
- 书籍与阅读物相关动作必须优先落到书籍区规则，不再把“零散散放在学习目录里”视为目标形态。
- 临时项目相关动作必须优先落到临时项目区规则，不再把“先丢在 workspace 根层，之后再说”视为目标形态。
- 临时治理文件相关动作必须优先落到临时文件区规则，不再把“先散放在 Human_Work_Zone 根层或下载目录里，之后再说”视为目标形态。
- 公司资料相关动作必须优先落到公司文档区规则，不再把“分散放在 GoogleDriveDump 或根层某个旧文件夹里”视为目标形态。
- 外部调研报告相关动作必须优先落到外部调研报告区规则，不再把“散放在 GoogleDriveDump、下载目录或临时文件夹里”视为目标形态。

## 局部规则
- 若用户明确点名 `Functional-HumenWorkZone-Manager`，默认不要越过 `Human_Work_Zone` 去操作其他目录。
- 若用户只是说“整理一下这个文件夹”，默认这里的“这个文件夹”就是 `Human_Work_Zone`。
- 若任务涉及开源项目，至少要同步考虑：
  - 集中管理区是否需要变更
  - inventory README 是否需要更新
  - 项目目录名是否符合 `<项目名>_<2-3word加强>` 规则
- 若任务涉及备份，至少要同步考虑：
  - 目标是否完整复制到了 `Backup_Management`
  - 备份目录名是否符合 `<2个word>_bak_<日期>` 规则
  - 备份 README 是否已经追加条目与一句描述
- 若任务涉及开源项目分析，至少要同步考虑：
  - 报告是否已经落到对应项目目录
  - 是否写清用户当时的问题与分析时间
  - 是否写清分析所针对的项目路径或版本上下文
  - 是否补了明确证据或证据入口
- 若任务涉及书籍或阅读物，至少要同步考虑：
  - 是否迁入了 `Books_and_Readings`
  - 名字是否符合统一命名规则
  - 根 README 是否已经追加或更新导航
  - 若该条目是资料包目录，是否需要包内 README
- 若任务涉及临时项目，至少要同步考虑：
  - 是否迁入了 `Temporary_Projects`
  - 项目目录名是否符合临时项目命名规则
  - `Temporary_Projects/README.md` 是否已经追加条目
  - 条目是否写清基础作用、项目 README 链接和当前状态
- 若任务涉及临时治理文件，至少要同步考虑：
  - 是否落到了 `Temporary_Files`
  - 当前任务更适合直接创建文件还是先创建一个主题子目录
  - `Temporary_Files/README.md` 是否已经追加条目
  - 条目是否写清文件或子目录路径、用途说明和当前状态
- 若任务涉及公司资料，至少要同步考虑：
  - 是否迁入了 `Company_Documents`
  - 公司目录名是否符合统一命名规则
  - `Company_Documents/README.md` 是否已经追加条目
  - 条目是否写清公司名、目录路径、资料作用和当前状态
- 若任务涉及外部调研报告，至少要同步考虑：
  - 是否迁入了 `External_Research_Reports`
  - 报告目录名、主报告文件名和资料包文件名是否符合统一命名规则
  - `External_Research_Reports/README.md` 是否已经追加条目
  - 条目是否写清主题、目录路径、主报告入口和当前状态
- 现有散落在 `Human_Work_Zone` 根层的开源 repo 视为 legacy placement；先纳入 inventory，再决定是否显式迁移。

## 例外与门禁
- 若用户要求的动作明显超出 `Human_Work_Zone`，应先显式指出范围已经越界。
- 若后续新增专属脚本、清单或规则文档，必须同步更新门面与 routing。
- 若用户没有明确要求，不要直接批量搬迁已存在的本地 repo；优先先建 inventory 与规则，再做显式迁移。
- 若用户要求“备份某个文件夹”，默认执行完整复制，不做裁剪、不做内容筛选、不改备份内部结构。
- 若用户针对开源项目提问，默认需要把答案沉淀成可追溯报告，而不是只在当轮对话给一句结论。
- 若用户要求整理书籍或阅读物，默认允许批量迁移和重命名，但应保持内容本体不变。
- 若用户要求收纳某个临时项目，默认允许整体迁移到 `Temporary_Projects`；除非用户明确要求，不自动删减内部内容。
- 若用户要求治理一批临时 markdown 或其他零散文件，默认允许把它们收纳到 `Temporary_Files`；模型可按当时意图决定文件名或主题子目录名，但不得越出该受管区。
- 若用户要求收纳公司资料，默认允许整体迁移到 `Company_Documents`；这一步只做收纳和命名，不提前替代未来的公司专属管理技能。
- 若用户要求收纳外部调研报告，默认允许整体迁移到 `External_Research_Reports`；这一步只做收纳、重命名和导航，不提前扩写成知识库。

## 下沉执行文档
- 开源项目集中区规则：`../runtime/OPEN_SOURCE_PROJECTS_ZONE_POLICY.md`
- 拉取开源项目流程：`../runtime/PULL_OPEN_SOURCE_PROJECT_FLOW.md`
- inventory README 维护流程：`../runtime/OPEN_SOURCE_PROJECT_README_MAINTENANCE_FLOW.md`
- 项目目录命名规则：`../runtime/OPEN_SOURCE_PROJECT_NAMING_RULE.md`
- 备份集中区规则：`../runtime/BACKUP_MANAGEMENT_ZONE_POLICY.md`
- 文件夹备份流程：`../runtime/CREATE_FOLDER_BACKUP_FLOW.md`
- 备份 README 维护流程：`../runtime/BACKUP_README_MAINTENANCE_FLOW.md`
- 备份目录命名规则：`../runtime/BACKUP_NAMING_RULE.md`
- 开源项目分析区规则：`../runtime/OPEN_SOURCE_PROJECT_ANALYSIS_ZONE_POLICY.md`
- 开源项目问答分析流程：`../runtime/ANSWER_OPEN_SOURCE_PROJECT_QUESTION_FLOW.md`
- 分析索引维护流程：`../runtime/PROJECT_ANALYSIS_INDEX_MAINTENANCE_FLOW.md`
- 分析报告结构规则：`../runtime/PROJECT_ANALYSIS_REPORT_STRUCTURE.md`
- 书籍区规则：`../runtime/BOOKS_AND_READINGS_ZONE_POLICY.md`
- 书籍整理流程：`../runtime/ORGANIZE_BOOKS_AND_READINGS_FLOW.md`
- 书籍导航维护流程：`../runtime/BOOK_LIBRARY_README_MAINTENANCE_FLOW.md`
- 书籍命名规则：`../runtime/BOOK_NAMING_RULE.md`
- 临时项目区规则：`../runtime/TEMPORARY_PROJECTS_ZONE_POLICY.md`
- 临时项目迁移流程：`../runtime/ORGANIZE_TEMPORARY_PROJECT_FLOW.md`
- 临时项目清单维护流程：`../runtime/TEMP_PROJECT_README_MAINTENANCE_FLOW.md`
- 临时项目命名规则：`../runtime/TEMP_PROJECT_NAMING_RULE.md`
- 临时文件区规则：`../runtime/TEMPORARY_FILES_ZONE_POLICY.md`
- 临时文件收纳流程：`../runtime/ORGANIZE_TEMPORARY_FILES_FLOW.md`
- 公司文档区规则：`../runtime/COMPANY_DOCUMENTS_ZONE_POLICY.md`
- 公司资料迁移流程：`../runtime/ORGANIZE_COMPANY_DOCUMENTS_FLOW.md`
- 公司清单维护流程：`../runtime/COMPANY_DOCUMENTS_README_MAINTENANCE_FLOW.md`
- 公司目录命名规则：`../runtime/COMPANY_FOLDER_NAMING_RULE.md`
- 外部调研报告区规则：`../runtime/EXTERNAL_RESEARCH_REPORTS_ZONE_POLICY.md`
- 外部调研报告迁移流程：`../runtime/ORGANIZE_EXTERNAL_RESEARCH_REPORTS_FLOW.md`
- 外部调研报告清单维护流程：`../runtime/EXTERNAL_RESEARCH_REPORTS_README_MAINTENANCE_FLOW.md`
- 外部调研报告命名规则：`../runtime/EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md`
