---
doc_id: workflow_sitemap_creation.references.policies.skill_execution_rules
doc_type: topic_atom
topic: Execution rules for Workflow-SiteMap-Creation
---

# Skill Execution Rules

## Runtime Rules

- 默认把每轮用户输入解释为双重目的输入，不接受“只更新产物不更新技能内部信号”的半执行模式。
- factory 后必须显式调用 `$Meta-Enhance-Prompt`，不得直接从 factory payload 跳到写盘。
- background subagent 必须通过 `tmux` 启动，模型固定 `gpt-5.4`，reasoning effort 固定 `high`。
- 主 AGENT 必须持续轮询 background subagent；只有连续 `10` 分钟无新输出时才允许判死。
- SUBAGENT 必须执行 `$Functional-Analysis-Runtask analysis_loop` 九阶段；中间阶段不得折叠。
- `design` 阶段必须显式用 `$Meta-keyword-first-edit` 决策删掉重写、keyword-first 替换或最小必要新增。
- 真源先写 `Octopus_OS/Development_Docs/mother_doc`，再刷新 `Octopus_OS/Client_Applications/mother_doc` 镜像。
- 产物架构禁止继续使用“文档知识库”叫法。
- 产物 lint 审计入口只使用技能自身承载的规则，不借用外部模糊判断。

## Architecture Rules

- 统一架构至少覆盖：
  - 全站开发文档
  - 代码地图
  - 使用说明书
  - 衍生说明
- 统一架构至少显式包含：
  - 治理层
  - 站点地图层
  - 代码地图层
  - 使用说明层
  - 运行治理层
- 新规则一旦进入本技能，就必须同时反映到说明文档、生成逻辑与 lint 规则，而不是只补说明文字。
- 产物刷新必须晚于 subagent 结果回读，且必须展示规则变化后的可观察框架形态。

## Runstate Rules

- `self_governance` 与 `artifact_lint_audit` 都必须引用 `workflow_runtime_checklist` 与 `stage_runtime_checklist`。
- 下一步必须消费上一步的结构化产物，不能跳步。
- runstate 必须显式记录 tmux 轮询、手工终止、九阶段 evidence sync 与 validation closeout。
