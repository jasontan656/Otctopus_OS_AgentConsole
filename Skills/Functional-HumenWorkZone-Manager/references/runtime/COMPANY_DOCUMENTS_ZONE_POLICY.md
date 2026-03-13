---
doc_id: functional_humenworkzone_manager.runtime.company_documents_zone_policy
doc_type: topic_atom
topic: Dedicated company-document zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends company-document tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The zone policy must obey the skill execution boundary.
- target: ORGANIZE_COMPANY_DOCUMENTS_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Intake and relocation are split into an operational flow.
- target: COMPANY_DOCUMENTS_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Inventory upkeep is managed as a separate maintenance flow.
- target: COMPANY_FOLDER_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Naming decisions are governed separately.
---

# Company Documents Zone Policy

## 目标目录
- 公司&文档集中管理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/Company_Documents`。
- 该目录用于承载各家公司对应的文档、图片、视频及其他公司资料目录。

## 目录职责
- 本目录当前只负责“集中收纳与导航”，不接管具体公司的业务管理。
- 本目录下必须长期维护 `README.md`，记录：
  - 当前有哪些公司目录
  - 每个公司目录的基础作用
  - 当前本地路径
  - 当前状态，例如：`active`、`paused`、`archive_candidate`

## 收纳原则
- 只要某个目录被判定为“以公司名承载的公司资料目录”，就应进入本区。
- 默认执行整目录迁移，不做内容裁剪，不改资料内部结构。
- 当前阶段只做收纳；具体公司管理能力后续交给新的专属技能。

## 进入本区后的后续分流
- 若要把外部公司资料目录迁入本区，进入 `ORGANIZE_COMPANY_DOCUMENTS_FLOW.md`。
- 若要维护公司清单或状态，进入 `COMPANY_DOCUMENTS_README_MAINTENANCE_FLOW.md`。
- 若要决定目录名或校验命名，进入 `COMPANY_FOLDER_NAMING_RULE.md`。
