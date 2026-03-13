---
doc_id: functional_humenworkzone_manager.runtime.external_research_reports_zone_policy
doc_type: topic_atom
topic: Dedicated external-research-report zone inside Human_Work_Zone
anchors:
- target: ../routing/TASK_ROUTING.md
  relation: implements
  direction: upstream
  reason: Task routing sends external-research-report tasks here.
- target: ../governance/SKILL_EXECUTION_RULES.md
  relation: governed_by
  direction: upstream
  reason: The zone policy must obey the skill execution boundary.
- target: ORGANIZE_EXTERNAL_RESEARCH_REPORTS_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Intake and relocation are split into an operational flow.
- target: EXTERNAL_RESEARCH_REPORTS_README_MAINTENANCE_FLOW.md
  relation: routes_to
  direction: downstream
  reason: Inventory upkeep is managed as a separate maintenance flow.
- target: EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md
  relation: routes_to
  direction: downstream
  reason: Naming decisions are governed separately.
---

# External Research Reports Zone Policy

## 目标目录
- 外部调研报告集中管理区固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/External_Research_Reports`。
- 该目录用于承载“从外部收集回来的调研报告、AI 汇总报告、报告资料包、附带证据文件与多媒体附件”。

## 目录职责
- 本目录当前只负责“集中收纳、统一命名与导航”，不直接替代知识库或专题研究系统。
- 本目录下必须长期维护 `README.md`，记录：
  - 当前有哪些调研报告目录
  - 每个目录的主题或对象
  - 主报告入口
  - 当前本地路径
  - 当前状态，例如：`active`、`paused`、`archive_candidate`

## 收纳原则
- 只要某个目录的主体价值是“一份对外部信息源的调研成果”，就应进入本区。
- 默认执行整目录迁移，不做内容裁剪，但允许按内容对目录和关键文件重命名。
- 重命名的目标是让用户一眼看出主题，而不是保留含糊的导出名或下载名。

## 进入本区后的后续分流
- 若要把外部调研报告目录迁入本区，进入 `ORGANIZE_EXTERNAL_RESEARCH_REPORTS_FLOW.md`。
- 若要维护调研报告清单或状态，进入 `EXTERNAL_RESEARCH_REPORTS_README_MAINTENANCE_FLOW.md`。
- 若要决定目录名、主报告文件名或资料包文件名，进入 `EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md`。
