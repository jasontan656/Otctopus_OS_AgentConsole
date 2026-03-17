---
doc_id: workflow_sitemap_creation.references.routing.task_routing
doc_type: topic_atom
topic: Task routing for Workflow-SiteMap-Creation
---

# Task Routing

- 当任务要把用户描述 factory 化、强化为 `INTENT:`、再经 background subagent 执行九阶段闭环并刷新产物时，进入 `path/self_governance/00_SELF_GOVERNANCE_ENTRY.md`。
- 当任务要对 `mother_doc` 真源或镜像执行 lint、审计或治理裁决时，进入 `path/artifact_lint_audit/00_ARTIFACT_AUDIT_ENTRY.md`。
- 稳定 profile 记录在 `references/profiles/SELECTED_PROFILE.md`。

## 固定路由判断

1. 用户描述中只要出现新架构设计、回写方式、文档分层、代码地图、说明书、规则固化、lint 思路、tmux subagent、九阶段 runtask 或治理工作流演进，就走 `self_governance`。
2. 用户描述中只要出现审计、lint、校验、门禁、差异检查或治理结论，就走 `artifact_lint_audit`。
3. 若同时出现两类目的，仍然先走 `self_governance`，因为本技能默认把输入视为双重目的输入且正式主链内含产物刷新与 validation closeout。

## 上下游边界

- 上游输入：用户回合描述。
- 当前技能输出：`Octopus_OS/Development_Docs/mother_doc` 真源架构、client mirror、技能内部演化信号，以及 runtask / subagent 闭环证据摘要。
- 下游消费者：`Workflow-MotherDoc-OctopusOS` 与后续 `construction_plan / implementation / acceptance`。
