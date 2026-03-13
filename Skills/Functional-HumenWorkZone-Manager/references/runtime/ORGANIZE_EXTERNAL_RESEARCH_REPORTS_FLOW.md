---
doc_id: functional_humenworkzone_manager.runtime.organize_external_research_reports_flow
doc_type: topic_atom
topic: Intake flow for external research reports
anchors:
- target: EXTERNAL_RESEARCH_REPORTS_ZONE_POLICY.md
  relation: implements
  direction: upstream
  reason: This flow operationalizes the external-research-report zone policy.
- target: EXTERNAL_RESEARCH_REPORTS_README_MAINTENANCE_FLOW.md
  relation: triggered_by
  direction: downstream
  reason: Every successful intake must update the report inventory.
- target: EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md
  relation: references
  direction: downstream
  reason: Intake requires a governed naming decision before relocation.
---

# Organize External Research Reports Flow

## 适用场景
- 用户要求把外部调研报告、报告资料包或 AI 整理回来的研究目录收纳到 `Human_Work_Zone`。
- 某个目录当前散放在 `GoogleDriveDump`、下载目录或其他临时位置，但应纳入长期可查的调研报告区。

## 固定动作
1. 先确认目标目录属于“外部调研报告”，而不是开源项目分析、书籍、备份或公司资料。
2. 先按 `EXTERNAL_RESEARCH_REPORT_NAMING_RULE.md` 判断目录名、主报告文件名和资料包文件名。
3. 目标落点固定为 `/home/jasontan656/AI_Projects/Human_Work_Zone/External_Research_Reports/<report-folder>/`。
4. 默认执行整目录迁移，而不是复制残留双份。
5. 迁移后允许对主报告、压缩资料包等关键文件重命名，但不改内部内容。
6. 迁移完成后，同 turn 更新 `External_Research_Reports/README.md`。

## 写回要求
- 至少登记这些字段：
  - 调研主题
  - 当前路径
  - 一句话基础说明
  - 主报告本地链接
  - 当前状态

## 默认状态
- 新迁入的调研报告默认状态写为 `active`。
- 若用户明确说明“只是留档，后面可能删”，可写成 `archive_candidate`。
